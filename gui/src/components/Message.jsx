


export const Message = ({message}) => {
	const { user } = useAuth();
	return (
		<div>
			<div className="bg-blue-500 text-white p-2 rounded-lg w-min my-1 self-start">
				{message.message}
			</div>
		</div>
	)
}
