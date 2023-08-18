import PriorityQueue from 'js-priority-queue';
import { EventEmitter } from 'events';

interface ChatMessage {
    message: MessageBody;
    priority: number;
}

interface MessageBody {
    type: string;
    user_name: string;
    content: string;
    expand: string;
}

export const chatPriorityQueue = new PriorityQueue<ChatMessage>({ comparator: (a, b) => a.priority - b.priority });
