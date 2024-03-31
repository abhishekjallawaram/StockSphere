import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation
import { cn } from '@/lib/utils'; // Ensure this utility function is correctly imported

// MainNav Functional Component
export function MainNav({ className, ...props }) {
  return (
    <nav className={cn('flex items-center space-x-4 lg:space-x-6', className)} {...props}>
      <Link to="/examples/dashboard" className="text-sm font-medium transition-colors hover:text-primary">
        Dashboard
      </Link>
      <Link to="/examples/dashboard" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
        Customers
      </Link>
      <Link to="/examples/dashboard" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
        Stock Analyze
      </Link>
      <Link to="/examples/dashboard" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
        Settings
      </Link>
    </nav>
  );
}

export default MainNav;
