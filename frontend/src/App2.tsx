import UserEditForm from '@/components/users/UserEditForm'
import { useFetchUsersQuery } from '@/hooks/apis/users'

function App() {
  const { data, isLoading, error } = useFetchUsersQuery()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>❌ Error: {(error as Error).message}</div>

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {data.users.map((item: any) => (
          <li key={item.id}>
            {item.id} - {item.name}
          </li>
        ))}
      </ul>
      <UserEditForm id="user1" currentName="やまだたろう" currentEmail="taro@example.com" />
    </div>
  )
}

export default App
