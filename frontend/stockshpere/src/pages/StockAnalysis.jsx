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



function StockAnalysis() {

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
            stock_id: stock.stock_id, // You will need to have the stock id in your stockData
            agent_id: 0, // You might have the user's id in the user object from local storage
            ticket: stock.Company_ticker,
            volume: volumeValue, // You should assign unique IDs to your volume inputs
            each_cost: stock.Closed_price,
            action: "buy"// The current date-time in ISO format
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
            <div className="flex flex-col">
                <nav className="flex justify-between items-center p-4 border-b">
                    <MainNav />
                    <UserNav />
                </nav>

                <div className="flex-1 overflow-hidden p-9">
                    <div className="flex justify-between items-center mb-4">
                        <h1 className="text-5xl font-bold p-9">Stock Analysis</h1>

                    </div>


                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4  ">


                        <div className="md:col-span-1 pr-8">

                            <h1 className="text-3xl text-left font-bold font-mono text-center md:text-left p-6  transition-colors hover:text-primary">Stocks : </h1>

                            <Card className="flex flex-col h-auto  h-[580px] mb-4 ml-2 w-[600px]"> 
     
                            
                            </Card>
                        </div>
                        
                        <div className="md:col-span-1  mt-14 ">
                        <h1 className="text-2xl text-left font-bold font-mono text-center md:text-left transition-colors hover:text-primary"> Your Stocks : </h1>
                            <div className="md:col-span-1 md:mt-8 max-h-12 ml">
                                <Card className="flex-grow w-[300px] rounded-md ml-1 mb-9"> {/* Adjust max-width as needed */}
                               
                                        <TableHeader >
                                            <TableRow className>
                                                <TableHead className="pl-12">Ticker</TableHead>
                                                <TableHead className=""> Bprice</TableHead>
                                                <TableHead className="">Volume</TableHead>
                                            </TableRow>
                                        </TableHeader>
                                    
                                    <ScrollArea className="h-[160px] mb-4 ml-3 w-[270px] rounded-md border p-4 "> {/* Set max height */}
                                        <CardContent>
                                            <TableBody className="items-center" >
                                                {cstockData.map((cstockData, index) => (
                                                    <TableRow key={index} >
                                                        <TableCell className="pl-1">{cstockData.stock_ticket}</TableCell>
                                                        <TableCell className="">{cstockData.each_cost}</TableCell>
                                                        <TableCell className="">{cstockData.volume}</TableCell>
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </CardContent>
                                    </ScrollArea>
                                </Card>
                                <h1 className="text-2xl text-left font-bold font-mono text-center md:text-left transition-colors hover:text-primary">Transactions : </h1>

                                <Card className="flex-grow w-[540px] mt-5 rounded-md ml "> {/* Adjust max-width as needed */}


                                        <TableHeader>
                                            <TableRow>
                                                <TableHead className="pl-14" >Date&nbsp;&nbsp;&nbsp;</TableHead>
                                                <TableHead className="pl-14"> time</TableHead>
                                                <TableHead className="pl-12">Ticker</TableHead>
                                                <TableHead className="pl-8">Action</TableHead>
                                                <TableHead>Volume</TableHead>
                                            </TableRow>
                                        </TableHeader>

                                    <ScrollArea className="h-[160px] w-[520px] mb-4 rounded-md ml-2 border p-4"> {/* Set max height */}
                                        <CardContent>

                                            <TableBody className="items-center" >
                                                {transaction.map((transaction, index) => (
                                                    <TableRow key={index} >
                                                        <TableCell >{new Date(transaction.date).toLocaleString().split(",")[0]}</TableCell>
                                                        <TableCell>{new Date(transaction.date).toLocaleString().split(",")[1]}</TableCell>
                                                        <TableCell className="pl-1">{transaction.ticket}</TableCell>
                                                        <TableCell className="pl-5">{transaction.action}</TableCell>
                                                        <TableCell className="pl-10 ">{transaction.volume}</TableCell>
                                                        <Separator />

                                                    </TableRow>
                                                ))}
                                            </TableBody>

                                        </CardContent>
                                    </ScrollArea>
                                </Card>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </>


    );
}
export default StockAnalysis;


