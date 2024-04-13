import React, { useState, useEffect } from 'react';
import { useLocalState } from './usingLocalStorage';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children, roleRequired }) => {
    const [jwt] = useLocalState("", "jwt");
    const [user, setUser] = useLocalState({}, "user"); // Assuming user is an object
    const [isLoading, setLoading] = useState(true);
    const [isValid, setIsValid] = useState(false);

    useEffect(() => {
        if (jwt) {
            (async () => {
                try {
                    const response = await fetch('http://localhost:8000/api/auth/test-token', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${jwt}`,
                        },
                    });
                    const data = await response.json();
                    if (response.ok) {
                        setUser(data);
                        setIsValid(true);
                    } else {
                        setIsValid(false);
                    }
                } catch (error) {
                    console.error('Error during user validation', error);
                    setIsValid(false);
                } finally {
                    setLoading(false);
                }
            })();
        } else {
            setLoading(false);
            setIsValid(false);
        }
    }, [jwt, setUser]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (!isValid || (roleRequired && user.role !== roleRequired)) {
        // Redirect to login if not valid, or not authorized based on role
        return <Navigate to="/login" replace />;
    }

    return children;
};
export default PrivateRoute;
