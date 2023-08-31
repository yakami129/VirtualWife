export const AssistantText = ({ message, role_name }: { message: string, role_name: string }) => {
  return (
    <div className="absolute bottom-0 left-0 mb-104  w-full">
      <div className="mx-auto max-w-4xl w-full p-16">
        <div className="bg-white rounded-8">
          <div className="px-24 py-8 bg-secondary rounded-t-8 text-white font-Montserrat font-bold tracking-wider">
            {role_name}
          </div>
          <div className="px-24 py-16">
            <div className="line-clamp-4 text-secondary typography-16 font-M_PLUS_2 font-bold">
              {message.replace(/\[([a-zA-Z]*?)\]/g, "")}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
