// components/TravelPlanCard.tsx
import React from 'react'
import { Card, Button, message } from 'antd'
import { ItineraryRequest } from '../api/chat'
import axios from 'axios'

interface Props {
  plan: string
  request: ItineraryRequest
}

const TravelPlanCard: React.FC<Props> = ({ plan, request }) => {
  const handleSave = async () => {
    try {
      const res = await axios.post('http://localhost:8000/itinerary/save', {
        id: crypto.randomUUID(),
        created_at: new Date().toISOString(),
        plan_text: plan,
        ...request
      })
      message.success('行程已保存，可分享')
    } catch (err) {
      message.error('保存失败')
    }
  }

  return (
    <Card title="🎒 为您定制的旅行计划" style={{ marginTop: 24 }}>
      <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>{plan}</pre>
      <Button type="primary" onClick={handleSave} style={{ marginTop: 16 }}>
        保存并生成分享卡片
      </Button>
    </Card>
  )
}

export default TravelPlanCard
