import PriorityQueue from 'js-priority-queue';
import { EventEmitter } from 'events';

interface ChatMessage {
    message: MessageBody;
    priority: number;
}

interface MessageBody {
    content: string;
    cmd: string;
    type: string;
}

export const chatPriorityQueue = new PriorityQueue<ChatMessage>({ comparator: (a, b) => a.priority - b.priority });
