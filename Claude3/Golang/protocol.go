package main

import (
	"context"

	"github.com/aws/aws-sdk-go-v2/service/bedrockruntime/types"
)

type StreamingOutputHandler func(ctx context.Context, part []byte) error
type ConverseStreamingOutputDeltaHandler func(ctx context.Context, part types.ContentBlockDelta) error
type ConverseStreamingOutputStartHandler func(ctx context.Context, part types.ContentBlockStart) error

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
