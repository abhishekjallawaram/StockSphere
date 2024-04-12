// import React, { useEffect, useState } from 'react';
// import { Button } from "@/components/ui/button";
// import {
//     Table,
//     TableBody,
//     TableCaption,
//     TableCell,
//     TableHead,
//     TableHeader,
//     TableRow,
// } from "@/components/ui/table"
// import { Input } from "@/components/ui/input";
// import { Label } from "@/components/ui/label";
// import { useNavigate } from "react-router-dom";
// import { useLocalState } from '@/utils/usingLocalStorage';
// import { UserNav } from './comp/user-nav';
// import { ScrollArea } from "@/components/ui/scroll-area"
// import { MainNav } from '@/components/ui/main-nav';
// import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
// import { Separator } from "@/components/ui/separator"

// import {
//     DropdownMenu,
//     DropdownMenuContent,
//     DropdownMenuItem,
//     DropdownMenuLabel,
//     DropdownMenuSeparator,
//     DropdownMenuTrigger,
// } from "@/components/ui/dropdown-menu"

// import {
//     Dialog,
//     DialogContent,
//     DialogDescription,
//     DialogHeader,
//     DialogTitle,
//     DialogTrigger,
// } from "@/components/ui/dialog"

// function Dashboard() {

//     const [stockData, setStockData] = useState([]);
//     const [cstockData, csetStockData] = useState([]);
//     const [AgentData, setAgentData] = useState([]);
//     const [transaction, setTransaction] = useState([]);
//     const [jwt, setJwt] = useLocalState("", "jwt");
//     const [user] = useLocalState("", "user");
//     const dropdownStyle = {
//         position: 'absolute', // Position absolutely to float over other content
//         right: 0, // Align to the right side of the parent container
//         zIndex: 1000, // Ensure it sits on top of other elements
//         width: '200px', // Set a fixed width or use max-width if you want it to be flexible
//     };

//     useEffect(() => {


//         const fetchStockData = async () => {
//             try {
//                 const requestOptions = {
//                     method: "GET",
//                     headers: {
//                         "Content-Type": "application/json",
//                         Authorization: "Bearer " + jwt,
//                     },
//                 };

//                 const response = await fetch('http://localhost:8000/api/stocks/', requestOptions);
//                 const data = await response.json();
//                 setStockData(data);
//             } catch (error) {
//                 console.error('Error fetching stock data:', error);
//             }
//         };

//         const fetchAgentData = async () => {
//             try {
//                 const requestOptions = {
//                     method: "GET",
//                     headers: {
//                         "Content-Type": "application/json",
//                         Authorization: "Bearer " + jwt,
//                     },
//                 };

//                 const response = await fetch('http://localhost:8000/api/agents/', requestOptions);
//                 const data = await response.json();
//                 setAgentData(data);
//             } catch (error) {
//                 console.error('Error fetching stock data:', error);
//             }
//         };


//         const fetchtransationData = async () => {
//             try {
//                 const requestOptions = {
//                     method: "GET",
//                     headers: {
//                         "Content-Type": "application/json",
//                         Authorization: "Bearer " + jwt,
//                     },
//                 };

//                 const response = await fetch('http://localhost:8000/api/transactions/', requestOptions);
//                 const data = await response.json();
//                 setTransaction(data);
//             } catch (error) {
//                 console.error('Error fetching setTransaction data:', error);
//             }
//         };

//         const fetchcstockData = async () => {
//             try {
//                 const requestOptions = {
//                     method: "GET",
//                     headers: {
//                         "Content-Type": "application/json",
//                         Authorization: "Bearer " + jwt,
//                     },
//                 };

//                 const response = await fetch('http://localhost:8000/api/transactions/customer-stocks', requestOptions);
//                 const data = await response.json();
//                 csetStockData(data);
//                 console.log(data);
//             } catch (error) {
//                 console.error('Error fetching setTransaction data:', error);
//             }
//         };

//         fetchStockData(), fetchtransationData(), fetchAgentData(), fetchcstockData();
//     }, [jwt]);
//     // console.log(transaction);


//     const handleBuy = async (stock) => {
//         // Assume you have the user's agent_id stored in user object
//         const volumeValue = parseInt(document.getElementById(`volume-${stock.Company_ticker}`).value, 10);
//         const transactionData = {
//             stock_id: stock.stock_id, 
//             agent_id: 0, 
//             ticket: stock.Company_ticker,
//             volume: volumeValue, 
//             each_cost: stock.Closed_price,
//             action: "buy"
//         };

//         try {
//             const requestOptions = {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     Authorization: "Bearer " + jwt,
//                 },
//                 body: JSON.stringify(transactionData),
//             };

//             const response = await fetch('http://localhost:8000/api/transactions/', requestOptions);

//             if (!response.ok) {
//                 const errorBody = await response.json();
//                 console.log('Failed to complete the transaction:', errorBody);
//                 throw new Error('Network response was not ok');
//             }

//             const data = await response.json();
//             console.log('Transaction successful', data);

//             // Update local transaction state to reflect the new transaction
//             setTransaction([...transaction, data]);
//         } catch (error) {
//             console.error('Failed to complete the transaction:', error);
//             // Log the error detail if it's available in the response
//             if (error.response && error.response.data && error.response.data.detail) {
//                 console.error('Transaction error details:', error.response.data.detail);
//                 // If it's an array, log the first element to see the specific error
//                 if (Array.isArray(error.response.data.detail)) {
//                     console.error('First validation error:', error.response.data.detail[0]);
//                 }
//             }
//         }
//     };



//     return (
//         <>
//             <div className="flex flex-col">
//                 <nav className="flex justify-between items-center p-4 border-b">
//                     <MainNav className="ml-12" />
//                     <UserNav  className ="mr-14-12"/>
//                 </nav>
//                 <div className="flex-1  overflow-hidden p-9 bg">
//                     <div className="flex justify-between grid grid-cols-2 md:grid-cols-2 items-center mb-4">
//                         <h1 className="text-5xl font-bold p-9">Dashboard</h1>
//                         <div className="text-2xl font-bold md:grid-cols-3  text-yellow-400">
//                             Balance: {user.balance}  
                            
//                             <div className="text-3xl font-bold"> 
//                                net_stock:  {user.net_stock}
//                             </div>
//                             </div>
//                     </div>


//                     <div className="grid grid-cols-1 md:grid-cols-2 gap-2  ">


//                         <div className="md:col-span-1 pr-8 ">

//                             <h1 className="text-3xl text-left font-bold font-mono text-center md:text-left p-6  transition-colors hover:text-primary">Stocks : </h1>

//                             <Card className="flex flex-col h-auto  h-[580px] mb-4 ml-16 w-[600px]"> {/* Adjust height as needed */}
//                                 {/* <CardTitle className="text-xl p-6 text-left">Stock Data</CardTitle> */}
//                                 <TableHeader className="items-center mt-2  ">
//                                     <TableRow>
//                                         <TableHead className="font-mono  transition-colors hover:text-primary  pl-16 w-1/4 ">CName</TableHead>
//                                         <TableHead className="  font-mono w-1/4 pl-16  transition-colors hover:text-primary">Ticker</TableHead>
//                                         <TableHead className="  font-mono w-1/4 pl-9  transition-colors hover:text-primary">ClPrice</TableHead>
//                                         <TableHead className=" font-mono  w-1/4 pl-6  transition-colors hover:text-primary"> PE:Ratio</TableHead>
//                                         {/* <TableHead className=" font-mono w-1/4 pl-6">Volune</TableHead>
//                                         <TableHead className=" font-mono w-1/4 pl-2">Agent</TableHead> */}

//                                         <TableHead className=" font-mono  w-1/4 pl-7  transition-colors hover:text-primary">Action</TableHead>
//                                     </TableRow>
//                                 </TableHeader>

//                                 <ScrollArea  className="h-[580px] mt-2 mb-4 ml-2 w-[580px] rounded-md border p-4">

//                                     <CardContent>
//                                         <TableBody className="" >
//                                             {stockData.map((stock, index) => (
//                                                 <TableRow key={index}>
//                                                     <TableCell className=" font-mono w-1/4 px-4 py-2" >{stock.Company_name}</TableCell>
//                                                     <TableCell className="font-mono">{stock.Company_ticker}</TableCell>
//                                                     <TableCell className="font-mono">${stock.Closed_price ? stock.Closed_price.toFixed(2) : 'N/A'}</TableCell>
//                                                     <TableCell className="font-mono">{stock.Company_PE ? stock.Company_PE.toFixed(2) : 'N/A'}</TableCell>
//                                                     <TableCell><Dialog>
//                                                         <DialogTrigger className=' transition-colors hover:text-primary w-1/4 pl-8' >Buy</DialogTrigger>
//                                                         <DialogContent>
//                                                             <DialogHeader>
                                                                
//                                                                 <Card className='w-[460px] mx-auto'>
//       <CardHeader className="space-y-1">
//         <CardTitle className="text-3xl">CART</CardTitle>
//         <CardDescription className="text-2xl">
//           Check your stock details
//         </CardDescription>


//         <CardContent>
//   <div className="flex flex-col space-y-4 p-4">
//     <div className='flex justify-between'>
//       <h3 className="text-1xl font-mono">Company Name:</h3>
//       <span className="text-1xl font-mono">{stock.Company_name}</span>
//     </div>
//     <div className='flex justify-between'>
//       <h3 className="text-1xl font-mono">Company Ticker:</h3>
//       <span className="text-1xl font-mono">{stock.Company_ticker}</span>
//     </div>
//     <div className='flex justify-between'>
//       <h3 className="text-1xl font-mono">Closed Price:</h3>
//       <span className="text-1xl font-mono">${stock.Closed_price.toFixed(2)}</span>
//     </div>
//     <div className='flex justify-between'>
//       <h3 className="text-1xl font-mono">Company PE:</h3>
//       <span className="text-1xl font-mono">{stock.Company_PE}</span>
//     </div>
//     <div className='flex justify-between items-center'>
//       <h2 className="text-1xl font-mono">Volume:</h2>
//       <Input
//         id={`volume-${stock.Company_ticker}`}
//         name="volume"
//         type="number"
//         defaultValue="1"
//         placeholder=""
//         className="w-1/3" // You may need to adjust this based on your layout
//       />
//     </div>
//     <div className='flex justify-between items-center'>
//       <h2 className="text-1xl font-mono">Agent :</h2>
//       <DropdownMenu>
//       <DropdownMenuTrigger>Select Agent</DropdownMenuTrigger>
//       <DropdownMenuContent>
//         <DropdownMenuLabel>Agents</DropdownMenuLabel>
//         <DropdownMenuSeparator />
//         {AgentData.map(agent => (
//           <DropdownMenuItem key={agent.agent_id}>{agent.name}</DropdownMenuItem>
//         ))}
//       </DropdownMenuContent>
//     </DropdownMenu>                           
//     </div>
//   </div>
// </CardContent>
//       </CardHeader>
     
//       <CardFooter className="flex flex-col gap-4">
//         <Button className="w-full" type="submit" onClick={()=>handleBuy(stock)}>BUY</Button>
//       </CardFooter>
//     </Card>
//                                                                 <DialogDescription>
                                                                    
//                                                                 </DialogDescription>
//                                                             </DialogHeader>
//                                                         </DialogContent>
//                                                     </Dialog></TableCell>

//                                                 </TableRow>
//                                             ))}
//                                         </TableBody>
//                                     </CardContent>
//                                 </ScrollArea>
//                             </Card>
//                         </div>
                        
//                         <div className="md:col-span-1  mt-14">
//                         <></>
//                         <div></div>
//                         <h1 className="text-2xl text-left font-bold font-mono text-center md:text-left transition-colors hover:text-primary"> Your Stocks : </h1>
//                             <div className="md:col-span-1 md:mt-8 max-h-12 ml  ">
//                             <div className='grid grid-cols-1 md:grid-cols-2 gap-' >
//                                 <Card className="flex-grow w-[300px] rounded-md  mb-9"> {/* Adjust max-width as needed */}
                               
//                                         <TableHeader >
//                                             <TableRow className>
//                                                 <TableHead className="pl-12">Ticker</TableHead>
//                                                 <TableHead className=""> Bprice</TableHead>
//                                                 <TableHead className="">Volume</TableHead>
//                                             </TableRow>
//                                         </TableHeader>
                                    
//                                     <ScrollArea className="h-[160px] mb-4 ml-3 w-[270px] rounded-md border p-4 "> {/* Set max height */}
//                                         <CardContent>
//                                             <TableBody className="items-center" >
//                                                 {cstockData.map((cstockData, index) => (
//                                                     <TableRow key={index} >
//                                                         <TableCell className="pl-1">{cstockData.stock_ticket}</TableCell>
//                                                         <TableCell className="">{cstockData.each_cost}</TableCell>
//                                                         <TableCell className="">{cstockData.volume}</TableCell>
//                                                     </TableRow>
//                                                 ))}
//                                             </TableBody>
//                                         </CardContent>
//                                     </ScrollArea>
//                                 </Card>
//                                 {/* <Card>
// <Label>   </Label>

//                                 </Card> */}
//                                 </div>
//                                 <h1 className="text-2xl text-left font-bold font-mono text-center md:text-left transition-colors hover:text-primary">Transactions : </h1>

//                                 <Card className="flex-grow w-[420px] mt-5 rounded-md ml "> {/* Adjust max-width as needed */}


//                                         <TableHeader>
//                                             <TableRow>
//                                                 <TableHead className="pl-14" >
//                     <span>Date & Time </span> {/* Display date */}
//      </TableHead>
                                    
//                                                 <TableHead className="pl-5">Ticker</TableHead>
//                                                 <TableHead className="pl-2">Action</TableHead>
//                                                 <TableHead>Volume</TableHead>
//                                                 {/* <TableHead>Amount</TableHead> */}
//                                             </TableRow>
//                                         </TableHeader>

//                                     <ScrollArea className="h-[160px] w-[400px] mb-4 rounded-md ml-2 border p-4"> {/* Set max height */}
//                                         <CardContent>

//                                             <TableBody className="items-center h-[30px]" >
//                                                 {transaction.map((transaction, index) => (
//                                                     <TableRow key={index} >
//                                                         <TableCell ><div className='flex flex-col'>
//                     <span>{new Date(transaction.date).toLocaleDateString()}</span> {/* Display date */}
//                     <span>{new Date(transaction.date).toLocaleTimeString()}</span> {/* Display time */}
//                 </div></TableCell>
//                                                         {/* <TableCell></TableCell> */}
//                                                         <TableCell className="pl-1">{transaction.ticket}</TableCell>
//                                                         <TableCell className="pl-5">{transaction.action}</TableCell>
//                                                         <TableCell className="pl-10 ">{transaction.volume}</TableCell>
//                                                         <Separator />

//                                                     </TableRow>
//                                                 ))}
//                                             </TableBody>

//                                         </CardContent>
//                                     </ScrollArea>
//                                 </Card>
//                             </div>
//                         </div>

//                     </div>
//                 </div>
//             </div>
//         </>


//     );
// }
// export default Dashboard;


