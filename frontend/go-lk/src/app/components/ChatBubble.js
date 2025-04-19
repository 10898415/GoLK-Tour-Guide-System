export default function ChatBubble({ message }) {
  const { sender, text, time, avatar } = message;
  const isUser = sender === "user";

  return (
    <div
      className={`flex mb-3 ${isUser ? "justify-end" : "justify-start"}`}
    >
      {/* Avatar (left for bot, right for user) */}
      {!isUser && (
        <img
          src={avatar}
          alt="avatar"
          className="h-8 w-8 rounded-full mr-2 object-cover"
        />
      )}

      {/* Bubble */}
      <div
        className={`rounded-md p-3 ${
          isUser ? "bg-blue-100" : "bg-gray-100"
        } max-w-sm`}
      >
        <p className="mb-1 text-sm">{text}</p>
        <p className="text-xs text-gray-500">{time}</p>
      </div>

      {/* User avatar on the right */}
      {isUser && (
        <img
          src={avatar}
          alt="avatar"
          className="h-8 w-8 rounded-full ml-2 object-cover"
        />
      )}
    </div>
  );
}
