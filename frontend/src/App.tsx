import Home from '@/pages/Home'
import Login from '@/pages/Login'
import Users from '@/pages/Users'
import { fetchAuthSession } from 'aws-amplify/auth'
import { useEffect, useState } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router'

function RequireAuth({ children }: { children: any }) {
  const [authenticated, setAuthenticated] = useState<boolean | null>(null)

  useEffect(() => {
    const getSession = async () => {
      try {
        const session = await fetchAuthSession()
        console.log(session)
        setAuthenticated(true)
      } catch {
        setAuthenticated(false)
      }
    }
    getSession()
  }, [])

  if (authenticated === null) return <p>Loading...</p>
  if (!authenticated) return <Navigate to="/login" />

  return children
}

function NotFound() {
  return <p>Not Found</p>
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/" element={<Login />} />
        <Route path="/auth/users" element={<Users />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}
