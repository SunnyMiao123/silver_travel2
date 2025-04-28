// src/pages/Home.tsx
import React, { useState, useRef, useEffect } from 'react'
import { Layout, Card, message as antdMessage } from 'antd'
import ChatInput from '../components/ChatInput'
import { v4 as uuidv4 } from 'uuid'

const { Content } = Layout

const BACKEND_WS = 'ws://localhost:8090/chatguide/ws/chat'

const Home: React.FC = () => {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')  // 用于拼接流式 token
  const [summary, setSummary] = useState('')
  const [data, setData] = useState<any>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const userId = useRef(uuidv4()).current

  useEffect(() => {
    // 每次 messages 更新后滚动到底部
    const chatContainer = document.getElementById("chat-container")
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight
    }
  }, [answer])  // 监听 answer 变化，自动滚动到底部

  const handleSubmit = () => {
    if (!question.trim()) return

    // 清空上次的流式内容
    setAnswer('')
    setSummary('')
    setData(null)

    // 连接 WebSocket
    const ws = new WebSocket(BACKEND_WS)
    wsRef.current = ws

    ws.onopen = () => {
      ws.send(JSON.stringify({ user_id: userId, message: question }))
    }

    ws.onmessage = (event) => {
      const text = event.data as string

      if (text === '[DONE]') {
        return
      }

      // 尝试解析最终的 JSON
      try {
        const msg = JSON.parse(text)
        setSummary(msg.content.summary)
        setData(msg.content.data)
        ws.close()
      } catch {
        // 流式消息，逐段追加
        setAnswer((prev) => prev + text)  // 拼接每个 token
      }
    }

    ws.onerror = (err) => {
      console.error('WebSocket 错误', err)
      antdMessage.error('与服务器通信出现问题')
      ws.close()
    }

    ws.onclose = () => {
      console.log('WebSocket 已关闭')
    }

    setQuestion('')
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Content style={{ maxWidth: 800, margin: '0 auto', padding: 24 }}>
        <Card title="智能出行助手">
          <ChatInput value={question} onChange={setQuestion} onSubmit={handleSubmit} />
        </Card>

        <Card title="AI 对话" style={{ marginTop: 24 }}>
          <div id="chat-container" style={{ maxHeight: '70vh', overflowY: 'auto', whiteSpace: 'pre-wrap' }}>
            <div>{answer || '等待后端流式推送...'}</div>
          </div>
        </Card>
      </Content>
    </Layout>
  )
}

export default Home
