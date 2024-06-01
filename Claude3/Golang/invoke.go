package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime/types"
)

func invoke(modelID string, msg string, system string) (string, error) {

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
