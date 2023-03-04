import React, { useState, useEffect, createRef, useRef} from 'react';
import tw from 'tailwind-styled-components';
import { FaUser } from 'react-icons/fa';
import {AiFillRobot} from "react-icons/ai";
import { AiFillCopy } from 'react-icons/ai';
import { postMessage } from '../services/API';
import { BeatLoader } from 'react-spinners';
import { v4 as uuidv4 } from 'uuid';
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import {materialDark} from 'react-syntax-highlighter/dist/cjs/styles/prism'
import remarkGfm from 'remark-gfm'

const TextWithMarkdownSupport = ({ msg }) => {
  return (
    <ReactMarkdown
	  remarkPlugins={[remarkGfm]}
      components={{
        code({ node, inline, className, children, ...props }) {
          return !inline ? (
			<div className="w-full px-5">
				<SyntaxHighlighter
				  style={materialDark}
				  language="python"
				  children={String(children).replace(/\n$/, "")}
				  customStyle={{
					borderRadius: '5px',
					padding: '10px',
					fontSize: '0.8rem',
					paddingLeft: '10px',
				  }}
				  wrapLongLines={true}
				  {...props}
				/>
			</div>
          ) : (
            <code className={className ? className : ""} {...props}>
              {children}
            </code>
          );
        }
      }}
    >
      {msg}
    </ReactMarkdown>
  )
};

const ChatWindow = tw.div`flex flex-col min-h-[90%] max-h-[90%]  bg-[#f1f5f9] focus:outline-none shadow-xl overflow-y-scroll scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100`;

const ChatMessage = ({ message, animationId, disableCopy}) => {
  const messageStyle = message.isUser ? 'bg-[#bfdbfe]' : 'bg-[#e2e8f0]';

  const [showCopyText, setShowCopyText] = useState(false);

  const handleCopyText = () => {
    navigator.clipboard.writeText(message.text);
    setShowCopyText(true);
    setTimeout(() => setShowCopyText(false), 1000);
  };

  return (
    <div className="flex flex-col mt-1">
      <div className={`whitespace-pre-line font-small pt-1 pl-2 text-left ${messageStyle}`}>
        {message.isUser ? <FaUser className="inline-block text-gray-600" /> : <AiFillRobot className="inline-block text-grey-600" />}
        <button className="float-right focus:outline-none" onClick={handleCopyText} disabled={(animationId === message.messageId) && disableCopy}>
          <div className="flex items-center">
            <span className={`transition-opacity ${showCopyText ? 'opacity-50' : 'opacity-0'}  font-small text-grey-8000`}>
              Copied!
            </span>
            <AiFillCopy className="inline-block text-gray-600 opacity-25 mr-4" />
          </div>
        </button>
      </div>
      <div className={`whitespace-pre-line font-small pt-1 pb-4 pl-2 text-left ${messageStyle}`}>
        <div className="h-0.5 bg-gray-400 w-full mb-1 opacity-5"></div>
        <div style={{ fontFamily: 'monospace' }} className={`font-medium text-left ${messageStyle}`}>
          {animationId === message.messageId ? (
            <BeatLoader color={message.isUser ? '#4299E1' : '#718096'} loading={true} size={10} />
          ) : (
            <TextWithMarkdownSupport msg={message.text} />
          )}
        </div>
      </div>
    </div>
  );
};

const InputBox = ({ value, onChange, onSend, disabled }) => {
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      onSend();
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <textarea
        className="whitespace-normal w-full h-24 p-4 mt-2 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
        value={value}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        placeholder="Type your message here..."
        disabled={disabled}
      />
      <button
        className={`py-8 mt-2 px-10 shadow-xl font-medium text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${disabled ? 'bg-gray-500 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'}`}
        onClick={onSend}
        disabled={disabled}
      >
        Send
      </button>
    </div>
  );
};


const ChatApp = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isWaitingResponse, setIsWaitingResponse] = useState(false);
  const [animationId, setAnimationId] = useState(null);
  const chatWindowRef = useRef(null);

  const handleSend = async () => {
    if (inputValue.trim() === '') return;


    const newMessage = { text: inputValue.trim(), messageId: uuidv4(), timestamp: Date.now(), isUser: true };
    setMessages((prevState) => [...prevState, newMessage]);
    setInputValue('');

    try {
      setIsWaitingResponse(true);
      const pcResponse = { text: null, messageId: uuidv4(), timestamp: Date.now(), isUser: false };
      setMessages((prevState) => [...prevState, pcResponse]);
      setAnimationId(pcResponse.messageId);
      const data = await postMessage(inputValue);
      setMessages((prevState) => prevState.map((message) => (message.messageId === pcResponse.messageId ? { ...message, text: data.response } : message)));

    } catch (error) {
      console.error(error);
    } finally {
      setIsWaitingResponse(false);
      setAnimationId(null);
    }
  };

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  const styles = {
    margin: 'auto',
    maxWidth: '80%',
    height: '90%',
    paddingTop: '20px',
    paddingBottom: '20px',
    display: 'flex',
    flexDirection: 'column',
  };

  useEffect(() => {
    chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
  }, [messages]);

  return (
    <div style={styles}>
      <ChatWindow ref={chatWindowRef}>
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} animationId={animationId} disableCopy={isWaitingResponse} />
        ))}
      </ChatWindow>
      <InputBox
        value={inputValue}
        onChange={handleChange}
        onSend={handleSend}
        disabled={isWaitingResponse}
      />
    </div>
  );
};

export default ChatApp;