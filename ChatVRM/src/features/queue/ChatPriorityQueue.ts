import PriorityQueue from 'js-priority-queue';
import { EventEmitter } from 'events';

interface ChatMessage {
    message: string;
    priority: number;
}

export const chatPriorityQueue = new PriorityQueue<ChatMessage>({ comparator: (a, b) => a.priority - b.priority });

export function addNewItem(item: ChatMessage) {
    chatPriorityQueue.queue(item);
}

