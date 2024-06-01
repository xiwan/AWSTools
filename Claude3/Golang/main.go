package main

import (
	"bufio"
	"context"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime"
)

const converseModel = true
const defaultRegion = "us-east-1"
const defaultModel = "claude3-sonnet"
const claudePromptFormat = "\n\nHuman: %s\n\nAssistant:"

var modelMap = map[string]string{
	"claude2":        "anthropic.claude-v2",
	"claude3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
	"claude3-haiku":  "anthropic.claude-3-haiku-20240307-v1:0",
	"mistral7b":      "mistral.mistral-7b-instruct-v0:2",
	"mixtral_8_7b":   "mistral.mixtral-8x7b-instruct-v0:1",
}
var brc *bedrockruntime.Client
var model *string
var verbose *bool

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

type Operation func(modelID string, text string, system string) (string, error)

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

		var ops Operation

		if converseModel {
			ops = converse
		} else {
			ops = invoke
		}

		response, err := ops(modelMap[*model], msg, "You are a helpful assistant!")
		if err != nil {
			log.Fatal(err)
		}
		chatHistory = msg + response
	}

}
