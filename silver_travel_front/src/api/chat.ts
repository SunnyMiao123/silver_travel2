// src/api/chat.ts
import axios from 'axios'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ItineraryRequest {
  start_city: string
  aim_city: string
  days: string
  budget: string
  interests: string[]
  avoid_types: string[]
}
const baseURL = import.meta.env.VITE_API_BASE_URL

// 发送聊天历史获取自然语言答复与结构状态
export const sendChatHistory = async (chatHistory: ChatMessage[]) => {
  const response = await axios.post(baseURL+'chatguide/fill_request', {
    chat_history: chatHistory
  })
  return response.data
}

// 提交结构化 request 获取完整旅行计划
export const generatePlan = async (request: ItineraryRequest) => {
  const response = await axios.post(baseURL+'itinerary/plan_by_llm', request)
  return response.data
}
