// Home.tsx（前端联动逻辑：显示“生成计划”按钮并触发调用）
import React, { useState } from 'react'
import { Layout, Card, message, Button } from 'antd'
import ChatInput from '../components/ChatInput'
import TravelPlanCard from '../components/TravelPlanCard'
import ChatHistory from '../components/ChatHistory'
import { sendChatHistory, generatePlan } from '../api/chat'
import { Footer } from 'antd/es/layout/layout'

const { Content } = Layout
interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

const Home = () => {
  const [input, setInput] = useState('')
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])
  const [reply, setReply] = useState('')
  const [request, setRequest] = useState(null)
  const [plan, setPlan] = useState('')
  const [status, setStatus] = useState<'incomplete' | 'complete' | null>(null)
  const [loading, setLoading] = useState(false)
  

  const handleSubmit = async () => {
    if (!input.trim()) return
    const newMessage: ChatMessage = { role: 'user', content: input }
    const updated = [...chatHistory, newMessage]
    setChatHistory(updated)
    setInput('')

    try {
      setLoading(true)
      const res = await sendChatHistory(updated)
      setReply(res.result)
      setStatus(res.status)
      const aiReply: ChatMessage = { role: 'assistant', content: res.result }
      setChatHistory([...updated, aiReply])
      if (res.status === 'complete') {
        setRequest(res.request)
        setPlan(res.plan)
      }
    } catch (e) {
      message.error('请求失败')
    } finally {
      setLoading(false)
    }
  }

  const handleGeneratePlan = async () => {
    if (!request) return
    try {
      setLoading(true)
      const res = await generatePlan(request)
      setPlan(res.plan)
    } catch {
      message.error('生成计划失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Content style={{ padding: '24px', width: '70%', margin: '0 auto'}}>
        <Card title="银发旅行助手" style={{ marginBottom: 24 }}>
          <ChatHistory messages={chatHistory} />
          
          {status === 'complete' && (
              <Button type="primary" onClick={handleGeneratePlan} style={{ marginTop: 16 }}>
                生成旅行计划
              </Button>
            )}
        </Card>
        {status === 'complete' && plan && request && (
          <TravelPlanCard plan={plan} request={request} />
        )}  
      </Content>
      <Footer style={{ padding: '24px', width: '70%', margin: '0 auto'}}>
        <Card title="银发旅行问答">
          <ChatInput value={input} onChange={setInput} onSubmit={handleSubmit} />
        </Card>
      </Footer>
    </Layout>
  )
}

export default Home
