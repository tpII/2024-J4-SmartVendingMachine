import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname
  const publicPaths = ['/login', '/sign-up', '/google-callback']
  const isPublicPath = publicPaths.includes(path)
  const authToken = request.cookies.get('authToken')?.value

  if (isPublicPath && authToken) {
    return NextResponse.redirect(new URL('/', request.url))
  }
  if (!authToken && !isPublicPath) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return NextResponse.next()
}

// Add your protected routes
export const config = {
  matcher: ['/', '/protected', '/api/:path*']
}