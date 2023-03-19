import React from 'react';
import sendIcon from '../img/send_black_24dp.svg';
import {useState, KeyboardEvent} from "react";

interface ChatComposeProps {
    onNewMessage: Function;
    isLoading: boolean;
}

const ChatCompose: React.FC<ChatComposeProps> = ({onNewMessage, isLoading}) => {
    const [question, setQuestion] = useState<string>('');

    const submitQuestion = () => {
        if (question.trim().length > 0 && !isLoading) {
            onNewMessage(question);
            setQuestion('');
        }
    };
    
    const onKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Enter' || e.keyCode === 13) {
            submitQuestion();
        }
    }

    return <div className={'chat-compose-container'}>
        <div className={'chat-compose-container-inner'}>
            <div className={'chat-compose-text-container'}>
                <input
                    type={'text'}
                    value={question}
                    maxLength={4000}
                    onKeyDown={onKeyDown}
                    onChange={(e) => {setQuestion(e.target.value);}}
                    className={'chat-compose-input'}
                    placeholder={'Ask a question here'}
                />
            </div>
            <div className={'send-btn-container'}>
                <img
                    onClick={submitQuestion}
                    className={'send-btn'}
                    src={sendIcon}
                />
            </div>
        </div>

    </div>;
};

export default ChatCompose;