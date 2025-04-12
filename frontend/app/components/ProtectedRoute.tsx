'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../lib/auth/auth-context';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRoles?: string[];
}

export default function ProtectedRoute({ children, requiredRoles = [] }: ProtectedRouteProps) {
  const { user, isLoading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If not loading and not authenticated, redirect to login
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }

    // If authenticated but doesn't have required roles, redirect to dashboard
    if (
      !isLoading &&
      isAuthenticated &&
      requiredRoles.length > 0 &&
      !requiredRoles.some(role => user?.roles.includes(role))
    ) {
      router.push('/');
    }
  }, [isLoading, isAuthenticated, user, router, requiredRoles]);

  // Show loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // If not authenticated or doesn't have required roles, don't render children
  if (!isAuthenticated) {
    return null;
  }

  if (requiredRoles.length > 0 && !requiredRoles.some(role => user?.roles.includes(role))) {
    return null;
  }

  // Render children if authenticated and has required roles
  return <>{children}</>;
}
