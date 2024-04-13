import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation
import { cn } from '@/lib/utils'; 
import { ModeToggle } from '../mode-toggle';

// Ensure this utility function is correctly imported

// MainNav Functional Component
export function AdminMainNav({ className, ...props }) {
  
  return (
    <nav className={cn('flex items-center space-x-4 lg:space-x-6', className)} {...props}>
      <ModeToggle/>
      <Link to="/admin/dashboard" className="text-sm font-medium transition-colors hover:text-primary  ">
        Transactions
      </Link>
      <Link to="/admin/" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary">
        Customers
      </Link>
      <Link to="/admin/" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary ">
        Stock Analysis
      </Link>
      <Link to="/admin/" className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary ">
        Crypto Data
      </Link>

      <h1 className='pl-12 text-2xl font-bold'>Admin Dashboard</h1>
  
    </nav>
  );
}

export default AdminMainNav;
