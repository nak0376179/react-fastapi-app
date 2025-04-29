import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import { expect, test } from 'vitest'
import App from './App'

test('renders learn react link', () => {
  render(<App />)
  const linkElement = screen.getByText(/Material UI Vite.js example in TypeScript/i)
  expect(linkElement).toBeInTheDocument()
})
