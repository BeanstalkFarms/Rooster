import React from "react";
import ChatMessage from "./ChatMessage";
import {MessageArray} from "../interfaces/MessageArray";
import {RefObject, useEffect, useRef} from "react";
import QuestionPrompt from "./QuestionPrompt";

interface ChatHistoryProps {
    messages: MessageArray,
    onSelectPrompt: Function,
    isLoading: Boolean
}

const ChatHistory: React.FC<ChatHistoryProps> = (
    {
        messages,
        onSelectPrompt,
        isLoading
    }) => {
    const bottomRef: RefObject<HTMLDivElement> = useRef(null);

    const getMessages = (): React.ReactNode[] => {
        return messages.map((item, index) => {
            return <ChatMessage key={index} from={item.from} message={item.message} source={item.source}/>
        });
    }

    const getEmptyDiv = (): React.ReactNode => {
        return <div className={'chat-bot-empty-history-container'}>
            <div className={'empty-history-title'}>Here's some questions you can ask</div>
            <QuestionPrompt onClick={onSelectPrompt} question={'What is Beanstalk?'}/>
            <QuestionPrompt onClick={onSelectPrompt} question={'How does Beanstalk work?'}/>
            <QuestionPrompt onClick={onSelectPrompt} question={'Where does yield come from in Beanstalk?'}/>
            <div className={'disclaimer'}>ANSWERS MAY BE INACCURATE</div>
        </div>;
    };

    useEffect(() => {
        // 👇️ scroll to bottom every time messages change
        bottomRef.current?.scrollIntoView({behavior: 'smooth'});
    }, [messages]);

    return <div className={'chat-bot-history-container'}>
        {
            messages.length ? getMessages() : getEmptyDiv()
        }
        {
            isLoading &&
            <div className={'chat-message-container'}>
                <div className={`chat-name Rooster`}>
                    Rooster
                </div>
                <div className={'chat-msg'}>
                    <div className="lds-ellipsis">
                        <div></div>
                        <div></div>
                        <div></div>
                        <div></div>
                    </div>
                </div>
            </div>
        }
        <div ref={bottomRef}/>
    </div>;
};

export default ChatHistory;