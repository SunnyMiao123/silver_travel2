// components/ChatHistory.tsx
import React, { useEffect, useRef } from 'react'
import { List, Avatar } from 'antd'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

interface Props {
  messages: ChatMessage[]
}

const ChatHistory: React.FC<Props> = ({ messages }) => {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div style={{ maxHeight: '60vh', overflowY: 'auto', padding: '12px 0' }}>
      <List
        dataSource={messages}
        renderItem={(item) => (
          <List.Item
            style={{
              justifyContent: item.role === 'user' ? 'flex-end' : 'flex-start',
              border: 'none'
            }}
          >
            {item.role === 'assistant' && <Avatar src="/robot.png" />}
            <div
              style={{
                background: item.role === 'user' ? '#d4f4ff' : '#f6f6f6',
                borderRadius: 12,
                padding: '8px 12px',
                maxWidth: '75%',
                whiteSpace: 'pre-wrap',
                marginLeft: item.role === 'user' ? 'auto' : 8,
                marginRight: item.role === 'user' ? 8 : 'auto',
                fontSize: 15
              }}
            >
              {item.content}
            </div>
            {item.role === 'user' && <Avatar src="/user.png" />}
          </List.Item>
        )}
      />
      <div ref={bottomRef} />
    </div>
  )
}

export default ChatHistory
