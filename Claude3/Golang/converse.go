package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime/document"
	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime/types"
)

func converse(modelID string, text string, system string) (string, error) {

	tool := map[string]interface{}{
		"type": "object",
		"properties": map[string]interface{}{
			"sign": map[string]interface{}{
				"type":        "string",
				"description": "The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ, and WKRP.",
			},
		},
		"required": []interface{}{"sign"},
	}

	marshaler := document.NewLazyDocument(tool)
	tools := types.ToolConfiguration{
		Tools: []types.Tool{
			&types.ToolMemberToolSpec{
				Value: types.ToolSpecification{
					Name:        aws.String("top_song"),
					Description: aws.String("Description"),
					InputSchema: &types.ToolInputSchemaMemberJson{
						Value: marshaler,
					},
				},
			},
		},
	}

	content := types.ContentBlockMemberText{
		Value: text,
	}

	msg := types.Message{
		Role:    "user",
		Content: []types.ContentBlock{&content},
	}

	sys := types.SystemContentBlockMemberText{
		Value: system,
	}

	output, err := brc.ConverseStream(context.Background(), &bedrockruntime.ConverseStreamInput{
		System:     []types.SystemContentBlock{&sys},
		Messages:   []types.Message{msg},
		ModelId:    aws.String(modelID),
		ToolConfig: &tools,
	})

	if err != nil {
		return "", err
	}

	var combinedResult string
	processConverseStreamingOutput(output,
		func(ctx context.Context, part types.ContentBlockDelta) error {
			switch d := part.(type) {
			case *types.ContentBlockDeltaMemberText:
				var chunk = d.Value
				fmt.Print(chunk)
				combinedResult += chunk
			case *types.ContentBlockDeltaMemberToolUse:
				var chunk = d.Value
				fmt.Print(*chunk.Input)

			}
			return nil
		},
		func(ctx context.Context, start types.ContentBlockStart) error {
			switch d := start.(type) {
			case *types.ContentBlockStartMemberToolUse:
				var chunk = d.Value
				fmt.Print(*chunk.Name)
				fmt.Print(*chunk.ToolUseId)
			}
			return nil
		},
	)
	return combinedResult, nil
}

func processConverseStreamingOutput(
	output *bedrockruntime.ConverseStreamOutput,
	handler ConverseStreamingOutputDeltaHandler,
	start ConverseStreamingOutputStartHandler) (Response, error) {

	resp := Response{}

	for event := range output.GetStream().Events() {
		switch v := event.(type) {
		case *types.ConverseStreamOutputMemberContentBlockDelta:
			handler(context.Background(), v.Value.Delta)
		case *types.ConverseStreamOutputMemberContentBlockStart:
			start(context.Background(), v.Value.Start)
			//print(1)
		case *types.ConverseStreamOutputMemberContentBlockStop:
			//print(2)
		case *types.ConverseStreamOutputMemberMetadata:
			//print(3)
		case *types.ConverseStreamOutputMemberMessageStart:
			//print(4)
		case *types.ConverseStreamOutputMemberMessageStop:
			//print(5)
		default:
			fmt.Println("union is nil or unknown type")
		}
	}
	return resp, nil
}
