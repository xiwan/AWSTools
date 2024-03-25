package main

import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime/types"
)

const defaultRegion = "us-east-1"
const defaultModel = "claude3-sonnet"

var modelMap = map[string]string{
	"claude2":        "anthropic.claude-v2",
	"claude3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
	"claude3-haiku":  "anthropic.claude-3-haiku-20240307-v1:0",
	"mistral7b":      "mistral.mistral-7b-instruct-v0:2",
	"mixtral_8_7b":   "mistral.mixtral-8x7b-instruct-v0:1",
}

var brc *bedrockruntime.Client

var model *string

func init() {

	region := os.Getenv("AWS_REGION")
	if region == "" {
		region = defaultRegion
	}

	cfg, err := config.LoadDefaultConfig(context.Background(), config.WithRegion(region))
	if err != nil {
		log.Fatal(err)
	}

	brc = bedrockruntime.NewFromConfig(cfg)
}

var verbose *bool

func main() {

	model = flag.String("model", defaultModel, "The model to use (e.g., claude2, claude3-sonnet, claude3-haiku, mistral7b, mixtral_8_7b)")

	verbose = flag.Bool("verbose", false, "setting to true will log messages being exchanged with LLM")
	flag.Parse()

	region := os.Getenv("AWS_REGION")
	if region == "" {
		region = defaultRegion
	}

	log.Printf("Amazon Bedrock [AWS_REGION: %s, model: %s, modeID: %s ]", region, *model, modelMap[*model])

	// Check if the provided model is valid
	if _, ok := modelMap[*model]; !ok {
		log.Fatalf("Invalid model: %s", *model)
	}

	reader := bufio.NewReader(os.Stdin)

	var chatHistory string

	for {
		fmt.Print("\nEnter your message: ")
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)

		msg := chatHistory + fmt.Sprintf(claudePromptFormat, input)

		response, err := send(modelMap[*model], msg)

		if err != nil {
			log.Fatal(err)
		}

		chatHistory = msg + response
	}
}

const claudePromptFormat = "\n\nHuman: %s\n\nAssistant:"

func send(modelID string, msg string) (string, error) {

	if *verbose {
		fmt.Println("[sending message]", msg)
	}

	var payloadBytes []byte
	var err error
	payload := Request{Prompt: msg, MaxTokensToSample: 2048}

	payloadBytes, err = json.Marshal(payload)
	if err != nil {
		return "", err
	}

	if *model == "mistral7b" || *model == "mixtral_8_7b" {
		payload := MistralRequest{Prompt: msg, MaxTokens: 2048}
		payloadBytes, err = json.Marshal(payload)
		if err != nil {
			return "", err
		}
	}

	if *model == "claude3-sonnet" || *model == "claude3-haiku" {
		payload := Claude3Request{Messages: []Message{Message{Role: "user", Content: msg}}, MaxTokens: 2048, Version: "bedrock-2023-05-31"}
		payloadBytes, err = json.Marshal(payload)
		if err != nil {
			return "", err
		}
	}

	output, err := brc.InvokeModelWithResponseStream(context.Background(), &bedrockruntime.InvokeModelWithResponseStreamInput{
		Body:        payloadBytes,
		ModelId:     aws.String(modelID),
		ContentType: aws.String("application/json"),
	})

	if err != nil {
		return "", err
	}

	resp, err := processStreamingOutput(output, func(ctx context.Context, part []byte) error {
		fmt.Print(string(part))
		return nil
	})

	if err != nil {
		log.Fatal("streaming output processing error: ", err)
	}

	return resp.Completion, nil
}

type StreamingOutputHandler func(ctx context.Context, part []byte) error

func processStreamingOutput(output *bedrockruntime.InvokeModelWithResponseStreamOutput, handler StreamingOutputHandler) (Response, error) {

	var combinedResult string
	resp := Response{}

	for event := range output.GetStream().Events() {
		switch v := event.(type) {
		case *types.ResponseStreamMemberChunk:

			//fmt.Println("payload", string(v.Value.Bytes))

			if *model == "mistral7b" || *model == "mixtral_8_7b" {
				var resp MistralResponse
				err := json.Unmarshal([]byte(string(v.Value.Bytes)), &resp)
				if err != nil {
					return Response{}, err
				}
				handler(context.Background(), []byte(resp.Outputs[0].Text))
				combinedResult += resp.Outputs[0].Text
			}

			if *model == "claude2" {
				var resp Response
				err := json.NewDecoder(bytes.NewReader(v.Value.Bytes)).Decode(&resp)
				if err != nil {
					return resp, err
				}

				handler(context.Background(), []byte(resp.Completion))
				combinedResult += resp.Completion
			}

			if *model == "claude3-sonnet" || *model == "claude3-haiku" {

				var resp Claude3Response

				err := json.NewDecoder(bytes.NewReader(v.Value.Bytes)).Decode(&resp)
				if err != nil {
					return Response{}, err
				}

				if resp.Delta.Type == "text_delta" {
					handler(context.Background(), []byte(resp.Delta.Text))
					combinedResult += resp.Delta.Text
				}

			}

		case *types.UnknownUnionMember:
			fmt.Println("unknown tag:", v.Tag)

		default:
			fmt.Println("union is nil or unknown type")
		}
	}

	resp.Completion = combinedResult

	return resp, nil
}

// request/response model
type Request struct {
	Prompt            string   `json:"prompt"`
	MaxTokensToSample int      `json:"max_tokens_to_sample"`
	Temperature       float64  `json:"temperature,omitempty"`
	TopP              float64  `json:"top_p,omitempty"`
	TopK              int      `json:"top_k,omitempty"`
	StopSequences     []string `json:"stop_sequences,omitempty"`
}

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type Claude3Request struct {
	Messages      []Message `json:"messages"`
	MaxTokens     int       `json:"max_tokens"`
	Temperature   float64   `json:"temperature,omitempty"`
	TopP          float64   `json:"top_p,omitempty"`
	TopK          int       `json:"top_k,omitempty"`
	StopSequences []string  `json:"stop_sequences,omitempty"`
	Version       string    `json:"anthropic_version"`
}

type MistralRequest struct {
	Prompt      string  `json:"prompt"`
	MaxTokens   int     `json:"max_tokens"`
	Temperature float64 `json:"temperature,omitempty"`
	TopP        float64 `json:"top_p,omitempty"`
	TopK        int     `json:"top_k,omitempty"`
}

type Response struct {
	Completion string `json:"completion"`
}

type MistralOutput struct {
	Text       string `json:"text"`
	StopReason string `json:"stop_reason"`
}

type MistralResponse struct {
	Outputs []Output `json:"outputs"`
}

type Output struct {
	Text       string `json:"text"`
	StopReason string `json:"stop_reason"`
}

type Claude3Response struct {
	Type  string    `json:"type"`
	Index int       `json:"index"`
	Delta TextDelta `json:"delta"`
}

type TextDelta struct {
	Type string `json:"type"`
	Text string `json:"text"`
}