import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Terminal } from "lucide-react";

const MainPage = () => {
    return (
        <div className="p-6 bg-gray-900 min-h-screen text-white">
            <h1 className="text-4xl font-bold mb-6">Vulnerability Testing Dashboard</h1>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                <Card className="bg-gray-800 rounded-2xl shadow-xl">
                    <CardContent>
                        <h2 className="text-xl font-semibold">Scan Network</h2>
                        <Button className="mt-4 w-full bg-blue-600 hover:bg-blue-700">Start Scan</Button>
                    </CardContent>
                </Card>
                <Card className="bg-gray-800 rounded-2xl shadow-xl">
                    <CardContent>
                        <h2 className="text-xl font-semibold">Analyze Logs</h2>
                        <Button className="mt-4 w-full bg-green-600 hover:bg-green-700">View Logs</Button>
                    </CardContent>
                </Card>
                <Card className="bg-gray-800 rounded-2xl shadow-xl">
                    <CardContent>
                        <h2 className="text-xl font-semibold">Generate Report</h2>
                        <Button className="mt-4 w-full bg-red-600 hover:bg-red-700">Export</Button>
                    </CardContent>
                </Card>
            </div>
            <div className="mt-6">
                <Button className="bg-gray-700 hover:bg-gray-800">
                    <Terminal className="inline-block mr-2" />
                    Open Terminal
                </Button>
            </div>
        </div>
    );
}

export default MainPage;
