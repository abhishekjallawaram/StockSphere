import React, { useEffect, useState } from 'react';
import { Button } from "@/components/ui/button";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { useLocalState } from '@/utils/usingLocalStorage';
import { UserNav } from './comp/user-nav';
import { ScrollArea } from "@/components/ui/scroll-area"
import { MainNav } from '@/components/ui/main-nav';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from "@/components/ui/separator"
import GridExample from '@/components/table';

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"

function Dashboard() {

    const [stockData, setStockData] = useState([]);
    const [cstockData, csetStockData] = useState([]);
    const [AgentData, setAgentData] = useState([]);
    const [transaction, setTransaction] = useState([]);
    const [jwt, setJwt] = useLocalState("", "jwt");
    const [user] = useLocalState("", "user");
    const dropdownStyle = {
        position: 'absolute', // Position absolutely to float over other content
        right: 0, // Align to the right side of the parent container
        zIndex: 1000, // Ensure it sits on top of other elements
        width: '200px', // Set a fixed width or use max-width if you want it to be flexible
    };

    useEffect(() => {


        const fetchStockData = async () => {
            try {
                const requestOptions = {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + jwt,
                    },
                };

                const response = await fetch('http://localhost:8000/api/stocks/', requestOptions);
                const data = await response.json();
                setStockData(data);
            } catch (error) {
                console.error('Error fetching stock data:', error);
            }
        };

        const fetchAgentData = async () => {
            try {
                const requestOptions = {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + jwt,
                    },
                };

                const response = await fetch('http://localhost:8000/api/agents/', requestOptions);
                const data = await response.json();
                setAgentData(data);
            } catch (error) {
                console.error('Error fetching stock data:', error);
            }
        };


        const fetchtransationData = async () => {
            try {
                const requestOptions = {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + jwt,
                    },
                };

                const response = await fetch('http://localhost:8000/api/transactions/', requestOptions);
                const data = await response.json();
                setTransaction(data);
            } catch (error) {
                console.error('Error fetching setTransaction data:', error);
            }
        };

        const fetchcstockData = async () => {
            try {
                const requestOptions = {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + jwt,
                    },
                };

                const response = await fetch('http://localhost:8000/api/transactions/customer-stocks', requestOptions);
                const data = await response.json();
                csetStockData(data);
                console.log(data);
            } catch (error) {
                console.error('Error fetching setTransaction data:', error);
            }
        };

        fetchStockData(), fetchtransationData(), fetchAgentData(), fetchcstockData();
    }, [jwt]);
    // console.log(transaction);


    const handleBuy = async (stock) => {
        // Assume you have the user's agent_id stored in user object
        const volumeValue = parseInt(document.getElementById(`volume-${stock.Company_ticker}`).value, 10);
        const transactionData = {
            stock_id: stock.stock_id, 
            agent_id: 0, 
            ticket: stock.Company_ticker,
            volume: volumeValue, 
            each_cost: stock.Closed_price,
            action: "buy"
        };

        try {
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + jwt,
                },
                body: JSON.stringify(transactionData),
            };

            const response = await fetch('http://localhost:8000/api/transactions/', requestOptions);

            if (!response.ok) {
                const errorBody = await response.json();
                console.log('Failed to complete the transaction:', errorBody);
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Transaction successful', data);

            // Update local transaction state to reflect the new transaction
            setTransaction([...transaction, data]);
        } catch (error) {
            console.error('Failed to complete the transaction:', error);
            // Log the error detail if it's available in the response
            if (error.response && error.response.data && error.response.data.detail) {
                console.error('Transaction error details:', error.response.data.detail);
                // If it's an array, log the first element to see the specific error
                if (Array.isArray(error.response.data.detail)) {
                    console.error('First validation error:', error.response.data.detail[0]);
                }
            }
        }
    };



    return (
         <>
        <div className="flex flex-col h-screen">
            <nav className="flex justify-between items-center p-4 border-b">
                <MainNav className="ml-10" />
                <UserNav className="mr-10" />
            </nav>
            <div className="flex-1 overflow-auto p-9">
                <h1 className="text-4xl font-bold mb-4">Dashboard</h1>
                <div className="container mx-auto">
                    <GridExample /> {/* The grid component is now part of the dashboard */}
                </div>
            </div>
        </div>
    </>


    );
}
export default Dashboard;


