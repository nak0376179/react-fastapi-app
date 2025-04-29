import { useUpdateUserMutation } from '@/hooks/apis/users'
import { useState } from 'react'

type Props = {
  id: string
  currentName: string
  currentEmail: string
}

export default function UserEditForm({ id, currentName, currentEmail }: Props) {
  const [name, setName] = useState(currentName)
  const [email, setEmail] = useState(currentEmail)

  const { mutate: updateUser, isPending, isSuccess, error } = useUpdateUserMutation()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    updateUser({
      id,
      data: {
        name: name.trim() || undefined,
        email: email.trim() || undefined
      }
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <div>
        <label className="block text-sm font-medium">名前</label>
        <input className="border px-2 py-1 rounded w-full" value={name} onChange={(e) => setName(e.target.value)} />
      </div>

      <div>
        <label className="block text-sm font-medium">メール</label>
        <input className="border px-2 py-1 rounded w-full" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>

      <button type="submit" disabled={isPending} className="bg-blue-600 text-white px-4 py-1 rounded">
        {isPending ? '更新中...' : '更新'}
      </button>

      {isSuccess && <p className="text-green-600">✅ 更新成功</p>}
      {error && <p className="text-red-600">❌ エラー: {(error as Error).message}</p>}
    </form>
  )
}
