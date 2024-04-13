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
import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
  } from "@/components/ui/resizable"
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

import { AgGridReact } from 'ag-grid-react'; // AG Grid Component
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the grid

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import AdminMainNav from '@/components/ui/Admin-main-nav';
import {
    useReactTable,
    createColumnHelper,
    flexRender,
    getCoreRowModel,
  } from "@tanstack/react-table";

function AdminDashboard() {

    const [stockData, setStockData] = useState([]);
    const [cstockData, csetStockData] = useState([]);
    const [AgentData, setAgentData] = useState([]);
    const [transaction, setTransaction] = useState([]);
    const [jwt, setJwt] = useLocalState("", "jwt");
    const [user] = useLocalState("", "user");
    const dropdownStyle = {
        position: 'absolute',
        right: 0,  
        zIndex: 1000, 
        width: '200px', 
    };

        // Row Data: The data to be displayed.
        // const [rowData, setRowData] = useState(transaction);
        
        // Column Definitions: Defines the columns to be displayed.
        const [colDefs, setColDefs] = useState([
            // { field: "transaction_id" },
          { field: "customer_name" },
        //   { field: "stock_id" },
          { field: "agent_name" },
          { field: "ticket" },
          { field: "volume" },
          { field: "each_cost" },
          { field: "action" },
          { field: "date" }

          
        ]);
        const autoSizeStrategy = {
            type: 'fitCellContents'
        };
        const pagination = true;

// sets 10 rows per page (default is 100)
        const paginationPageSize = 10;

        // allows the user to select the page size from a predefined list of page sizes
        const paginationPageSizeSelector = [10, 20, 50, 100];
       

      
    useEffect(() => {





        const fetchtransationData = async () => {
            try {
                const requestOptions = {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + jwt,
                    },
                };

                const response = await fetch('http://localhost:8000/api/transactions/adminpro/', requestOptions);
                const data = await response.json();
                setTransaction(data);
            } catch (error) {
                console.error('Error fetching setTransaction data:', error);
            }
        };


         fetchtransationData();
    }, [jwt]);
    console.log(transaction);


    return (
        <>
            <div className="flex flex-col">
                <nav className="flex justify-between items-center p-4 border-b">
                    <AdminMainNav className="ml-12" />
                    <UserNav  className ="mr-14-12"/>
                </nav>
             
                
<Card className="justify-center m-24  w-[935px]" > 
                <div
  className="ag-theme-quartz justify-center" // applying the grid theme
  style={{ height: 540 , width : 930} } // the grid will fill the size of the parent container
 >
   <AgGridReact
       rowData={transaction}
       columnDefs={colDefs}
       autoSizeStrategy={autoSizeStrategy}
       pagination={pagination}
       paginationPageSize={paginationPageSize}
       paginationPageSizeSelector={paginationPageSizeSelector}
   />
 </div>
 </Card>
            </div>
        </>


    );
}

export default AdminDashboard;


