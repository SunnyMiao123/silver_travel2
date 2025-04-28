// src/components/ChatInput.tsx

import React from 'react'
import { Input, Button } from 'antd'

interface Props {
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  onSend: () => void
  disabled?: boolean
}

const ChatInput: React.FC<Props> = ({ value, onChange, onSend, disabled }) => {
  return (
    <div style={{ display: 'flex', gap: '10px' }}>
      <Input
        value={value}
        onChange={onChange}
        onPressEnter={onSend}
        placeholder="请输入内容..."
        disabled={disabled}
      />
      <Button type="primary" onClick={onSend} disabled={disabled}>
        发送
      </Button>
    </div>
  )
}

export default ChatInput
