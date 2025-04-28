// src/components/ChatHistory.tsx
import React from 'react'
import { ChatMessage } from '../types'
import '../styles/ChatHistory.css' // 假设你有一个 CSS 文件来处理样式
import ReactMarkdown from 'react-markdown'

interface Props {
  messages: ChatMessage[]
}

const ChatHistory: React.FC<Props> = ({ messages }) => {
  return (
    <div className="chat-history">
      {messages.map((msg, index) => (
        <div key={index} className={`chat-bubble ${msg.role}`}>
          {msg.role === 'assistant' ? (
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          ) : (
            msg.content
          )}
          <div className="timestamp">
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      ))}
    </div>
  )
}

export default ChatHistory