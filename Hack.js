import React, { useState } from 'react';
import { Send, Bot } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

const FAQChatbot = () => {
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Hello! How can I help you today?' }
  ]);
  const [inputValue, setInputValue] = useState('');

  // FAQ database
  const faqData = {
    'business hours': 'We are open Monday to Friday, 9 AM to 6 PM.',
    'payment methods': 'We accept credit cards, PayPal, and bank transfers.',
    'shipping': 'Orders typically ship within 2-3 business days.',
    'return policy': 'Items can be returned within 30 days of purchase.',
    'contact': 'You can reach our support team at support@example.com',
    'pricing': 'Our pricing details can be found on our pricing page. Basic plan starts at $10/month.',
    'account': 'To create an account, click the Sign Up button in the top right corner.',
    'password reset': 'You can reset your password by clicking "Forgot Password" on the login page.',
  };

  // Function to find best matching response
  const findResponse = (input) => {
    const normalizedInput = input.toLowerCase();
    
    // Check for exact matches first
    for (const [key, value] of Object.entries(faqData)) {
      if (normalizedInput.includes(key)) {
        return value;
      }
    }

    // If no exact match, provide a fallback response
    return "I'm not sure about that. Could you try rephrasing your question? You can ask about our business hours, payment methods, shipping, returns, contact information, pricing, account creation, or password reset.";
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const newMessages = [
      ...messages,
      { role: 'user', content: inputValue }
    ];

    // Add bot response
    const botResponse = findResponse(inputValue);
    newMessages.push({ role: 'bot', content: botResponse });

    setMessages(newMessages);
    setInputValue('');
  };

  return (
    <Card className="w-full max-w-md mx-auto h-[500px] flex flex-col">
      <CardContent className="flex flex-col h-full p-4">
        <div className="flex-grow overflow-y-auto space-y-4 mb-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100'
                }`}
              >
                {message.role === 'bot' && (
                  <Bot className="inline-block w-4 h-4 mr-2 mb-1" />
                )}
                {message.content}
              </div>
            </div>
          ))}
        </div>
        
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your question..."
            className="flex-grow p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </CardContent>
    </Card>
  );
};

export default FAQChatbot;