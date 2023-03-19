export interface Message {
    message: string;
    from: string;
    source: string | null;
}

export type MessageArray = Message[];
