import ChatHistory from "./ChatHistory";
import roosterLogo from '../img/BeanAI.svg';
import beanLogo from '../img/bean-logo.svg';
import ChatCompose from "./ChatCompose";
import {useState} from "react";
import {MessageArray} from "../interfaces/MessageArray";
import {loadQuestion} from "../API";

const ChatBot = () => {
    const [messages, setMessages] = useState<MessageArray>([]);
    const [loading, setLoading] = useState<boolean>(false);

    const addMessage = (from: string, message: string, source: string | null) => {
        const newMessage = { from, message, source};
        setMessages(messages => [...messages, newMessage]);
    };

    const getHistory = ():string => {
        const nameTranslation: Record<string, string> = {'You': 'Anon', 'Rooster': 'You'};
        return messages.slice(messages.length-3).map(message => `${nameTranslation[message.from]}: ${message.message}`).join('\n');
    };

    const onNewQuestion = async (message: string) => {
        setLoading(true);
        addMessage('You', message, null);
        let history = getHistory();

        //truncate history to last 2000 characters
        const maxCharacters = 2000;
        if (history.length > maxCharacters) {
            history = history.substring(history.length - maxCharacters);
        }
        const response = (await loadQuestion(message, history));
        let answer = response.answer;
        let source = response.source;

        if (answer === 'I\'m not sure.') {
            answer = 'I\'m not sure — I\'m only trained on the Farmers\' Almanac at the moment.';
            source = 'https://docs.bean.money/almanac/';
        }

        addMessage('Rooster', answer, source);
        setLoading(false);
    };

    const openHomepage = () => {
        window.open('https://bean.money/', '_blank');
    }

    const clearChat = () => {
        setMessages([]);
    }

    return (
    <div className={'chat-bot-container'}>
        <div className={'home-link-container'} onClick={openHomepage}>
            <img className={'bean-logo'} src={beanLogo}/>
            <div className={'home-text'}>Home</div>
        </div>
        <div className={'chat-bot-header'}>
            <img className={'rooster-logo'} src={roosterLogo} onClick={clearChat}/>
            <div className={'title'}>Rooster</div>
            <div className={'desc'}>Understand Beanstalk with the magic of AI</div>
        </div>
        <ChatHistory
            onSelectPrompt={onNewQuestion.bind(this)}
            messages={messages}
            isLoading={loading}
        />
        <ChatCompose onNewMessage={onNewQuestion} isLoading={loading} />
    </div>)
};

export default ChatBot;