import React from "react";

interface ChatMessageProps {
    from: string;
    message: string;
    source: string | null;
}

const ChatMessage: React.FC<ChatMessageProps> = ({from, message, source}) => {
    return (<div>
        <div className={'chat-message-container'}>
            <div className={`chat-name ${from}`}>
                {from}
            </div>
            <div className={'chat-msg'}>
                {message}
            </div>
            {source && <a href={source} target={'_blank'} rel="noreferrer" className={'chat-source'}>View source</a>}
        </div>
    </div>)
};

export default ChatMessage;