interface QuestionPromptProps {
    question: string,
    onClick: Function
}

const QuestionPrompt: React.FC<QuestionPromptProps> = ({question, onClick}) => {
    return <div
        className={'question-prompt'}
        onClick={onClick.bind(this, question)}
    >
        {question}
    </div>
}

export default QuestionPrompt;