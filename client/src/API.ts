const baseURL = window.location.href.includes("localhost") ? 'http://localhost:5001' : '/api';

export interface QuestionResponse {
    answer: string;
    source: string | null;
}

export async function loadQuestion(question: string, history: string): Promise<QuestionResponse> {
    try {
        const response = await fetch(`${baseURL}/ask?` + new URLSearchParams({ query: question, history}));
        return await response.json();
    } catch (e) {
        console.error(e);
        return {
            answer: "Something went wrong... Try again later.",
            source: null
        };
    }
}