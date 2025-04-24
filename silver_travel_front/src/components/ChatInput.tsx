import React from 'react'
import { Input, Button, Space } from 'antd'

const { TextArea } = Input

interface ChatInputProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
}

const ChatInput: React.FC<ChatInputProps> = ({ value, onChange, onSubmit }) => {
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <TextArea
        rows={4}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="请输入您的出行需求，例如：我想去杭州三天两晚，预算2000元"
      />
      <Button type="primary" onClick={onSubmit}>发送</Button>
    </Space>
  )
}

export default ChatInput