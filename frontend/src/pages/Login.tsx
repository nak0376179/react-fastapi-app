import { idTokenAtom } from '@/stores/auth'
import { fetchAuthSession, signIn } from 'aws-amplify/auth'
import { useSetAtom } from 'jotai'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const setIdToken = useSetAtom(idTokenAtom)
  const navigate = useNavigate()

  useEffect(() => {
    const checkLogin = async () => {
      const session = await fetchAuthSession().catch(() => null) // ログイン済みでなければ null
      console.log(session)
      const token = session?.tokens?.idToken?.toString() ?? null
      if (token) {
        setIdToken(token)
        navigate('/auth/users')
      }
    }
    checkLogin()
  }, [])

  const handleLogin = async () => {
    try {
      await signIn({ username, password })
      const session = await fetchAuthSession().catch(() => null) // ログイン済みでなければ null
      console.log(session)
      const token = session?.tokens?.idToken?.toString() ?? null
      setIdToken(token)
      navigate('/auth/users')
    } catch (err) {
      console.error('ログイン失敗:', err)
    }
  }
  return (
    <div>
      <input value={username} onChange={(e) => setUsername(e.target.value)} />
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" />
      <button onClick={handleLogin}>ログイン</button>
    </div>
  )
}

export default Login
