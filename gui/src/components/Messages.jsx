
import { Message } from "./Message";

export const MessageList = ({messages}) => {
	return (
		<ul>
		  {messages && messages.map((message, i) => <Message key={i} message={message} />)}
		</ul>
	)
}