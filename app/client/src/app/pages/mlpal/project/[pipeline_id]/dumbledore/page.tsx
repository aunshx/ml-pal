'use client'

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  ArrowDown,
  Bot,
  Clock,
  Dot,
  FileEdit,
  Send,
  User,
  ChevronDown,
  XCircle,
} from "lucide-react";
import {
  ResizablePanel,
  ResizablePanelGroup,
  ResizableHandle,
} from "@/components/ui/resizable";
import { Pipeline, usePipelineContext } from "@/context/PipelineContext";


export default function NewProjectPage() {
  const { pipelines } = usePipelineContext();
  const pathname = window.location.pathname;
  const targetPipelineId = pathname.split('/')[4];
  const pipeline = pipelines.find(pipeline => {
    return pipeline.pipeline_id === parseInt(targetPipelineId)
  })
  const [currentPipeline, setCurrentPipeline] = useState<Pipeline>(pipeline as Pipeline)
  console.log('OFJONOE', currentPipeline)
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      content: {
        title: "MLpal",
        body: "Sure, I'd be happy to help! Could you please provide more details about your task? For example, what kind of medical data are you working with, and what do you want to classify?",
      },
    },
    {
      id: 2,
      type: "user",
      content: {
        title: "You",
        body: "Hi, I need help building a machine learning model for a medical classification task.",
      },
    },
  ]);

  const [inputValue, setInputValue] = useState("");
  const [typingMessage, setTypingMessage] = useState("");
  const [typingId, setTypingId] = useState<number | null>(null);
  const [showScrollToBottom, setShowScrollToBottom] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationInterval, setGenerationInterval] = useState<string | null>(null);

  const [isEditing, setIsEditing] = useState(false);
  const [projectName, setProjectName] = useState("No Title");

  const [currentPhase, setCurrentPhase] = useState("Model Selection"); // Track current phase

  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);

  const randomReplies = [
    "Interesting question! Can you provide more details?",
    "I need to think about that. Let me get back to you.",
    "That's a great topic! What specifically do you want to know?",
    "Let's dive into that. What are your main concerns?",
    "Could you clarify what you mean by that?",
  ];

  const getRandomReply = () => {
    const randomIndex = Math.floor(Math.random() * randomReplies.length);
    return randomReplies[randomIndex];
  };

  const typeMessage = (message:any, speed = 25) => {
    let i = 0;
    setTypingMessage("");
    const interval = setInterval(() => {
      setTypingMessage((prev) => prev + message[i]);
      i++;
      if (i >= message.length) {
        // Changed condition
        clearInterval(interval);
        setGenerationInterval(null);
        setIsGenerating(false);
        setTypingId(null); // Clear typingId to finish typing effect
      }
    }, speed); // Adjust the speed here
    setGenerationInterval(interval);
  };

  const handleSend = () => {
    if (inputValue.trim() && !isGenerating) {
      const userMessage = {
        id: Date.now(),
        type: "user",
        content: {
          title: "You",
          body: inputValue,
        },
      };
      const botReply = {
        id: Date.now() + 1,
        type: "bot",
        content: {
          title: "MLpal",
          body: getRandomReply(),
        },
      };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInputValue("");
      setIsGenerating(true);
      setTypingId(botReply.id);
      setTimeout(() => {
        setMessages((prevMessages) => [...prevMessages, botReply]);
        typeMessage(botReply.content.body);
      }, 500);
    } else if (isGenerating) {
      stopGenerating();
    }
  };

  const stopGenerating = () => {
    if (generationInterval) {
      clearInterval(generationInterval);
      setGenerationInterval(null);
      setIsGenerating(false);
      setTypingId(null); // Clear typingId to finish typing effect
    }
  };

  const handleKeyDown = (e: any) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSend();
    }
  };

  const handleScroll = () => {
    if (messagesContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } =
        messagesContainerRef.current;
      setShowScrollToBottom(scrollTop + clientHeight < scrollHeight - 20);
    }
  };

  const scrollToBottom = () => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop =
        messagesContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (!isGenerating) {
      setTypingMessage("");
    }
  }, [messages]);

  return (
    <div className="flex h-full bg-background text-foreground">
      {/* Sidebar */}
      <div className="w-1/4 p-4 bg-secondary overflow-y-auto">
        <div className="flex items-center justify-between text-xl font-bold">
          {isEditing ? (
            <Input
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              onBlur={() => setIsEditing(false)}
              autoFocus
            />
          ) : (
            <>
              <h2 className="text-lg font-bold">{projectName}</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsEditing(true)}
              >
                <FileEdit className="w-5 h-5" />
              </Button>
            </>
          )}
        </div>
        <div className="mt-8 flex flex-col justify-between p-4 min-h-[200px]">
          <div
            className={`flex items-center space-x-2 ${
              currentPhase === "Model Selection" ? "font-bold" : ""
            }`}
            onClick={() => setCurrentPhase("Model Selection")}
          >
            <Clock className="w-5 h-5" />
            <span>Model Selection</span>
          </div>
          <div
            className={`flex items-center space-x-2 ${
              currentPhase === "Training" ? "font-bold" : ""
            }`}
            onClick={() => setCurrentPhase("Training")}
          >
            <Dot className="w-5 h-5" />
            <span>Training</span>
          </div>
          <div
            className={`flex items-center space-x-2 ${
              currentPhase === "Inference" ? "font-bold" : ""
            }`}
            onClick={() => setCurrentPhase("Inference")}
          >
            <ArrowDown className="w-5 h-5" />
            <span>Inference</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1">
        <ResizablePanelGroup direction="horizontal">
          {/* New Section */}
          {currentPhase === "Training" && (
            <>
              <ResizablePanel className="p-4 bg-gray-200 border-r border-border">
                <h3 className="text-xl font-bold">Training Phase Details</h3>
                <p>
                  This section contains details and options for the training
                  phase.
                </p>
              </ResizablePanel>
              <ResizableHandle withHandle />
              <ResizablePanel className="flex-1 flex flex-col">
                {/* Chat Area */}
                <div
                  className="flex-1 overflow-y-auto p-4 relative"
                  ref={messagesContainerRef}
                  onScroll={handleScroll}
                >
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex items-start space-x-4 mb-4 ${
                        message.type === "user"
                          ? "justify-end"
                          : "justify-start"
                      }`}
                    >
                      {message.type === "user" ? (
                        <>
                          <div className="p-3 bg-primary text-primary-foreground rounded-lg max-w-[70%]">
                            <p className="break-words">
                              {message.content.body}
                            </p>
                          </div>
                          <User className="w-6 h-6 flex-shrink-0 text-primary" />
                        </>
                      ) : (
                        <>
                          <Bot className="w-6 h-6 flex-shrink-0 text-secondary-foreground" />
                          <div className="p-3 bg-secondary text-secondary-foreground rounded-lg max-w-[70%]">
                            <p
                              className={`break-words ${
                                typingId === message.id ? "typewriter" : ""
                              }`}
                            >
                              {typingId === message.id
                                ? typingMessage
                                : message.content.body}
                            </p>
                          </div>
                        </>
                      )}
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>

                {/* Scroll to Bottom Button */}
                {showScrollToBottom && (
                  <Button
                    variant="secondary"
                    size="icon"
                    className="absolute bottom-20 right-6 shadow-md rounded-full"
                    onClick={scrollToBottom}
                  >
                    <ChevronDown className="w-6 h-6" />
                  </Button>
                )}

                {/* Input Area */}
                <div className="p-4 border-t border-border">
                  <div className="flex items-center">
                    <Input
                      type="text"
                      placeholder="Type your prompt ..."
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      onKeyDown={handleKeyDown}
                      className="flex-1"
                      disabled={isGenerating}
                    />
                    <Button
                      variant="ghost"
                      size="icon"
                      className="ml-2"
                      onClick={handleSend}
                    >
                      {isGenerating ? (
                        <XCircle className="w-6 h-6" />
                      ) : (
                        <Send className="w-6 h-6" />
                      )}
                    </Button>
                  </div>
                </div>
              </ResizablePanel>
            </>
          )}

          {/* Chat Area Only (for other phases) */}
          {currentPhase !== "Training" && (
            <ResizablePanel className="flex-1 flex flex-col pl-4 pt-4 ">
              <div
                className="flex-1 overflow-y-auto p-4 relative"
                ref={messagesContainerRef}
                onScroll={handleScroll}
              >
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex items-start space-x-4 mb-4 ${
                      message.type === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    {message.type === "user" ? (
                      <>
                        <div className="p-3 bg-primary text-primary-foreground rounded-lg max-w-[70%]">
                          <p className="break-words">{message.content.body}</p>
                        </div>
                        <User className="w-6 h-6 flex-shrink-0 text-primary" />
                      </>
                    ) : (
                      <>
                        <Bot className="w-6 h-6 flex-shrink-0 text-secondary-foreground" />
                        <div className="p-3 bg-secondary text-secondary-foreground rounded-lg max-w-[70%]">
                          <p
                            className={`break-words ${
                              typingId === message.id ? "typewriter" : ""
                            }`}
                          >
                            {typingId === message.id
                              ? typingMessage
                              : message.content.body}
                          </p>
                        </div>
                      </>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>

              {/* Scroll to Bottom Button */}
              {showScrollToBottom && (
                <Button
                  variant="secondary"
                  size="icon"
                  className="absolute bottom-20 right-6 shadow-md rounded-full"
                  onClick={scrollToBottom}
                >
                  <ChevronDown className="w-6 h-6" />
                </Button>
              )}

              {/* Input Area */}
              <div className="p-4 border-t border-border">
                <div className="flex items-center">
                  <Input
                    type="text"
                    placeholder="Type your prompt ..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="flex-1"
                    disabled={isGenerating}
                  />
                  <Button
                    variant="ghost"
                    size="icon"
                    className="ml-2"
                    onClick={handleSend}
                  >
                    {isGenerating ? (
                      <XCircle className="w-6 h-6" />
                    ) : (
                      <Send className="w-6 h-6" />
                    )}
                  </Button>
                </div>
              </div>
            </ResizablePanel>
          )}
        </ResizablePanelGroup>
      </div>
    </div>
  );
}
