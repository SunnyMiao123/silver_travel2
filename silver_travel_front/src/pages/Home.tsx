import {
  CommentOutlined,
  QuestionCircleOutlined,
  SmileOutlined,
  ScheduleOutlined,
  ProductOutlined,
  FileSearchOutlined,
  AppstoreAddOutlined,
  PlusOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons';
import {
  Bubble,
  Prompts,
  Sender,
  Welcome,
  Conversations,
} from '@ant-design/x';
import type { BubbleDataType } from '@ant-design/x/es/bubble/BubbleList';
import { Button, Flex, type GetProp, Space, message,  Avatar } from 'antd';
import { createStyles, css, keyframes,createGlobalStyle } from 'antd-style';
import dayjs from 'dayjs';
import React, { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import logo from '../assets/logo.png';


// 适合银发出行助手场景的推荐问题
const TRAVEL_PROMPTS: GetProp<typeof Prompts, 'items'> = [
 
];

const DEFAULT_CONVERSATIONS_ITEMS = [
  {
    key: 'default-0',
    label: 'What is Ant Design X?',
    group: 'Today',
  },
  {
    key: 'default-1',
    label: 'How to quickly install and import components?',
    group: 'Today',
  },
  {
    key: 'default-2',
    label: 'New AGI Hybrid Interface',
    group: 'Yesterday',
  },
];

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const GlobalStyle = createGlobalStyle(() => {
  return {
    'ant-bubble-content': {
      width: '70%',
    }}}
  );

const useStyle = createStyles(({ token }) => {
  return {
    
    layout: css`
      width: 100%;
      min-width: 360px;
      height: 100vh;
      display: flex;
      background: ${token.colorBgContainer};
      font-family: AlibabaPuHuiTi, ${token.fontFamily}, sans-serif;
      font-size: 14px;
    `,
    sider: css`
      background: ${token.colorBgLayout}80;
      width: 280px;
      height: 100%;
      display: flex;
      flex-direction: column;
      padding: 0 12px;
      box-sizing: border-box;
    `,
    logo: css`
      display: flex;
      align-items: center;
      padding: 16px 0;
      font-size: 20px;
      font-weight: 600;
      color: ${token.colorText};
      img {
        margin-right: 8px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        object-fit: cover;
      }
    `,
    addBtn: css`
      background: #1677ff0f;
      border: 1px solid #1677ff34;
      height: 40px;
    `,
    conversations: css`
      flex: 1;
      overflow-y: auto;
      margin-top: 12px;
      padding: 0;

      .ant-conversations-list {
        padding-inline-start: 0;
      }
    `,
    siderFooter: css`
    border-top: 1px solid ${token.colorBorderSecondary};
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  `,
    chat: css`
      height: 100%;
      width: 100%;
      max-width: 600px;
      margin: 0 auto;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      padding: ${token.paddingLG}px;
      gap: 16px;
      font-size: 14px;

    `,
    chatPrompt: css`
      .ant-prompts-label {
        color: #000000e0 !important;
        font-size: 14px !important;
      }
      .ant-prompts-desc {
        color: #000000a6 !important;
        width: 100%;
        font-size: 14px !important;
      }
      .ant-prompts-icon {
        color: #000000a6 !important;
        font-size: 20px !important;
      }
    `,
    chatList: css`
      flex: 1;
      overflow: auto;
      padding-right: 10px;
      font-size: 14px;
    `,
    bubble: css`
      font-size: 14px !important;
      letter-spacing: 1px;
      line-height: 1.7;
      animation: ${fadeIn} 0.3s ease forwards;
      a {
        color: #1890ff;
        text-decoration: underline;
      }
      img {
        max-width: 100%;
        border-radius: 8px;
        margin-top: 8px;
      }
      pre {
        background: #f5f5f5;
        padding: 8px;
        border-radius: 4px;
        overflow: auto;
      }
      code {
        background: #f5f5f5;
        padding: 2px 4px;
        border-radius: 4px;
      }
      p{
        margin-bottom:0px;
      }
      
    `,
    sender: css`
      box-shadow: ${token.boxShadow};
      color: ${token.colorText};
      font-size: 14px !important;
    `,
    senderPrompt: css`
      color: ${token.colorText};
      font-size: 14px;
      padding-bottom: 8px;
    `,
    placeholder: css`
      padding-top: 32px;
    `,
    avatar: css`
      width: 36px;
      height: 36px;
      border-radius: 50%;
      object-fit: cover;
    `,
  };
});

interface MessageItem {
  role: 'user' | 'assistant';
  content: string;
  id: string;
  isStreaming?: boolean;
}

const userAvatar = 'https://cdn-icons-png.flaticon.com/512/147/147144.png'; // user avatar placeholder
const assistantAvatar = 'https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*s5sNRo5LjfQAAAAAAAAAAAAADgCCAQ/fmt.webp'; // assistant avatar placeholder


const SilverTravelChat: React.FC = () => {
  const { styles } = useStyle();

  // Global styles for chat bubbles
  //GlobalStyle(()=>{});

  // WebSocket ref
  const wsRef = useRef<WebSocket | null>(null);
  const abortController = useRef<AbortController>(null);

  // Messages state
  const [messages, setMessages] = useState<MessageItem[]>([]);

  // Input value state
  const [inputValue, setInputValue] = useState('');

  // Loading state to disable input during response
  const [loading, setLoading] = useState(false);

  const [recording, setRecording] = React.useState(false);

  const [conversations, setConversations] = useState(DEFAULT_CONVERSATIONS_ITEMS);
  const [curConversation, setCurConversation] = useState(DEFAULT_CONVERSATIONS_ITEMS[0].key);

  // Buffer for streaming assistant message content
  const assistantBuffer = useRef<string>('');

  // Unique user_id for session, can be generated or fixed for demo
  const userId = useRef<string>('user_' + Math.random().toString(36).substr(2, 9));

  // Scroll to bottom ref
  const scrollRef = useRef<HTMLDivElement | null>(null);

  // Effect: initialize WebSocket connection
  useEffect(() => {
    // Connect to WebSocket server
    // Production: replace with production ws URL
    const ws = new WebSocket('ws://localhost:8090/chatguide/ws/chat');
    wsRef.current = ws;

    ws.onopen = () => {
      // console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = event.data;

      if (typeof data !== 'string') {
        return;
      }

      // New check: if data is JSON string with intent, agent, content fields, skip processing
      const trimmedData = data.trim();
      if (
        trimmedData.startsWith('{') &&
        trimmedData.endsWith('}')
      ) {
        try {
          const parsed = JSON.parse(trimmedData);
          if (
            parsed &&
            typeof parsed === 'object' &&
            'intent' in parsed &&
            'agent' in parsed &&
            'content' in parsed
          ) {
            return;
          }
        } catch {
          // not a valid JSON, continue processing
        }
      }

      // Handle special [DONE] message indicating end of stream
      if (data.trim() === '[DONE]') {
        // Finalize current assistant message
        if (assistantBuffer.current.trim().length > 0) {
          const newMessage: MessageItem = {
            role: 'assistant',
            content: assistantBuffer.current,
            id: Date.now().toString(),
            isStreaming: false,
          };
          setMessages((prev) => {
            // replace last streaming message with finalized one
            if (prev.length > 0 && prev[prev.length - 1].role === 'assistant' && prev[prev.length - 1].isStreaming) {
              return [...prev.slice(0, -1), newMessage];
            }
            return [...prev, newMessage];
          });
          assistantBuffer.current = '';
        }
        setLoading(false);
        return;
      }

      // Append chunk to buffer
      assistantBuffer.current += data;

      // Update last assistant message in messages or add a new one with typing animation
      setMessages((prev) => {
        // If last message is assistant and is streaming, update it
        if (prev.length > 0 && prev[prev.length - 1].role === 'assistant' && prev[prev.length - 1].isStreaming) {
          const last = prev[prev.length - 1];
          const updated = { ...last, content: assistantBuffer.current };
          return [...prev.slice(0, -1), updated];
        } else {
          // Add new assistant message with streaming flag
          const newMsg: MessageItem = {
            role: 'assistant',
            content: assistantBuffer.current,
            id: Date.now().toString(),
            isStreaming: true,
          };
          return [...prev, newMsg];
        }
      });
    };

    ws.onerror = (event) => {
      //message.error('WebSocket 连接错误，请刷新页面重试');
      setLoading(false);
    };

    ws.onclose = () => {
      // console.log('WebSocket closed');
      setLoading(false);
    };

    return () => {
      ws.close();
    };
  }, []);

  // Scroll to bottom when messages update
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  // Send message function
  const onSubmit = (val: string) => {
    if (!val.trim()) return;
    if (loading) {
      message.error('正在回复，请稍候');
      return;
    }
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      message.error('连接未建立，请稍后再试');
      return;
    }

    // Add user message immediately
    const userMessage: MessageItem = {
      role: 'user',
      content: val,
      id: Date.now().toString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    // Clear assistant buffer and loading state
    assistantBuffer.current = '';
    setLoading(true);

    // Send message via WebSocket as JSON string
    const payload = {
      user_id: userId.current,
      message: val,
    };
    wsRef.current.send(JSON.stringify(payload));

    setInputValue('');
  };

  // Custom bubble content, assistant messages always rendered as markdown, no typing animation
  const renderBubbleContent = (item: MessageItem) => {
    if (item.role === 'assistant') {
      // Always render assistant message (streaming or not) as markdown, no typing animation
      return <ReactMarkdown className={styles.bubble}>{item.content}</ReactMarkdown>;
    }
    // User message plain text
    return <div className={styles.bubble}>{item.content}</div>;
  };

  // Chat list component
  const chatList = (
    <div className={styles.chatList} ref={scrollRef}>
      {messages?.length ? (
        <Bubble.List
          items={messages.map((i) => ({
            content: renderBubbleContent(i),
            role: i.role,
            style:{width: '100%'},
            classNames: { content: styles.bubble },
            typing: !!i.isStreaming,
            avatar: (
              <img
                src={i.role === 'user' ? userAvatar : assistantAvatar}
                alt={i.role}
                className={styles.avatar}
                draggable={false}
              />
            ),
          }))}
          style={{ height: '100%' }}
          roles={{
            assistant: {
              placement: 'start',
              
            },
            user: {
              placement: 'end',
              
            },
          }}
        />
      ) : (
        <Space direction="vertical" size={16} className={styles.placeholder}>
          <Welcome
      icon="https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*s5sNRo5LjfQAAAAAAAAAAAAADgCCAQ/fmt.webp"
      title="您好，欢迎使用银发出行助手"
      description="我可以帮助您解决出行问题，您可以问我任何问题，比如：
              - 你能帮我推荐一个适合老年人的旅游目的地吗？
              - 我想知道去北京的最佳旅游时间是什么时候？
      "
          />
          <Prompts
            items={TRAVEL_PROMPTS}
            onItemClick={(info) => {
              onSubmit(info.data.description as string);
            }}
            styles={{
              item: {
                padding: '12px 24px',
                borderRadius: 16,
                margin: 4,
                background: 'linear-gradient(123deg, #e5f4ff 0%, #efe7ff 100%)',
                fontSize: 14,
                minHeight: 36,
              },
              list: { width: '100%', display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center' },
            }}
            className={styles.chatPrompt}
          />
        </Space>
      )}
    </div>
  );

  const chatSender = (
    <>
      <Prompts
        items={TRAVEL_PROMPTS}
        onItemClick={(info) => {
          onSubmit(info.data.description as string);
        }}
        styles={{
          item: {
            padding: '10px 18px',
            borderRadius: 12,
            fontSize: 14,
            background: 'linear-gradient(123deg, #e5f4ff 0%, #efe7ff 100%)',
            margin: 2,
          },
          list: { width: '100%', display: 'flex', flexWrap: 'wrap', gap: 8 },
        }}
        className={styles.senderPrompt}
      />
      <Sender
        value={inputValue}
        onSubmit={() => {
          onSubmit(inputValue);
        }}
        onChange={setInputValue}
        allowSpeech={{
          recording,
          onRecordingChange: (nextRecording) => {
            message.info(`Mock Customize Recording: ${nextRecording}`);
            setRecording(nextRecording);
          },
        }}
        loading={loading}
        className={styles.sender}
        actions={(_, info) => {
          const { SendButton, LoadingButton,SpeechButton } = info.components;
          return(
          <Space>
            <SpeechButton />
            {loading ? <LoadingButton type="primary" style={{ fontSize: 20 }} /> : <SendButton type="primary" style={{ fontSize: 20 }} />}
          </Space>)
      }}
        style={{
          fontSize: 20,
          height: 52,
        }}
        placeholder="请输入您的出行问题…"
      />
    </>
  );

  const chatSider = (
    <div className={styles.sider}>
      {/* 🌟 Logo */}
      <div className={styles.logo}>
        <img
          src={logo}
          draggable={false}
          alt="logo"
          width={50}
          height={50}
        />
        <span>银发旅行助手</span>
      </div>

      {/* 🌟 添加会话 */}
      <Button
        onClick={() => {
          const now = dayjs().valueOf().toString();
          setConversations([
            {
              key: now,
              label: `New Conversation ${conversations.length + 1}`,
              group: 'Today',
            },
            ...conversations,
          ]);
          setCurConversation(now);
          setMessages([]);
        }}
        type="link"
        className={styles.addBtn}
        icon={<PlusOutlined />}
      >
        New Conversation
      </Button>

      {/* 🌟 会话管理 */}
      <Conversations
        items={conversations}
        className={styles.conversations}
        activeKey={curConversation}
        onActiveChange={async (val) => {
          abortController.current?.abort();
          // The abort execution will trigger an asynchronous requestFallback, which may lead to timing issues.
          // In future versions, the sessionId capability will be added to resolve this problem.
          setTimeout(() => {
            setCurConversation(val);
          //  setMessages(messageHistory?.[val] || []);
          }, 100);
        }}
        groupable
        styles={{ item: { padding: '0 8px' } }}
        menu={(conversation) => ({
          items: [
            {
              label: 'Rename',
              key: 'rename',
              icon: <EditOutlined />,
            },
            {
              label: 'Delete',
              key: 'delete',
              icon: <DeleteOutlined />,
              danger: true,
              onClick: () => {
                const newList = conversations.filter((item) => item.key !== conversation.key);
                const newKey = newList?.[0]?.key;
                setConversations(newList);
                // The delete operation modifies curConversation and triggers onActiveChange, so it needs to be executed with a delay to ensure it overrides correctly at the end.
                // This feature will be fixed in a future version.
                setTimeout(() => {
                  if (conversation.key === curConversation) {
                    setCurConversation(newKey);
                   // setMessages(messageHistory?.[newKey] || []);
                  }
                }, 200);
              },
            },
          ],
        })}
      />

      <div className={styles.siderFooter}>
        <Avatar size={24} />
        <Button type="text" icon={<QuestionCircleOutlined />} />
      </div>
    </div>
  );

  return (
    <div className={styles.layout}>
      {chatSider}
      <div className={styles.chat}>
        {chatList}
        {chatSender}
      </div>
    </div>
  );
};

export default SilverTravelChat;