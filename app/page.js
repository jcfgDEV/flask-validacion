'use client'
import React, { useState } from "react";
import { ImWarning } from 'react-icons/im';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


export default function Page() {

    const [Enviar, setInfo] = useState({
        Nombre: '',
        Season: '',
        Date: '',
        Number: '',
    })

    const [Errors, setErrors] = useState({
        Nombre: [],
        Season: [],
        Date: [],
        Number: [],
    })

    const Change = (e) => {
        const { name, value } = e.target;
        setInfo(prevState => ({
            ...prevState,
            [name]: value
        }));

        setErrors({
            ...Errors,
            [name]: [],
        });
    };



    const handler = async (e) => {
        e.preventDefault();
        const res = await fetch('https://flask-validate-extenso-backend.vercel.app/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                Enviar
            }),
        });
        const response = await res.json();
        try {
            if (res.status === 200) {
                toast.success(`inserted data: ${response.id}`, {
                    position: "top-left",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    theme: "colored",
                });
                setInfo({
                    Nombre: '',
                    Season: '',
                    Date: '',
                    Number: '',
                })
            } else {
                setErrors(response.errors)
            }
        } catch (err) {
            //  console.log(err)
        }
    }






    return (
        <>
            <ToastContainer />
            <form onSubmit={handler} className="flex justify-center">
                <div className=" translate-y-20 w-[400px]">
                    <div className="mb-1">
                        {Errors.Nombre.map((error) => (
                            <div className=" text-red-600 flex items-center gap-1" key={error}><ImWarning className="text-red-500" />{error}</div>
                        ))}
                        <label className="block text-gray-700 font-bold mb-2" htmlFor="Nombre">
                            Name
                        </label>
                        <input
                            className={`border ${Errors.Nombre.length > 0 ? 'border-red-500' : ''} rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none`}
                            id="Nombre"
                            name="Nombre"
                            type="text"
                            placeholder="Jose, Andrea etc..."
                            onChange={Change}
                            value={Enviar.Nombre}
                        />
                    </div>
                    <div className="mb-1">
                        {Errors.Date.map((error) => (
                            <div className="text-red-600 flex items-center gap-1" key={error}><ImWarning className="text-red-500" />{error}</div>
                        ))}
                        <label className="block text-gray-700 font-bold mb-2" htmlFor="fecha">
                            Date
                        </label>
                        <input
                            className={`border ${Errors.Date.length > 0 ? 'border-red-500' : ''} rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none`}
                            id="fecha"
                            name="Date"
                            type="text"
                            placeholder="AAAA-MM-DD"
                            onChange={Change}
                            value={Enviar.Date}
                        />
                    </div>
                    <div className="mb-1">
                        {Errors.Number.map((error) => (
                            <div className=" text-red-600 flex items-center gap-1" key={error}><ImWarning className="text-red-500" />{error}</div>
                        ))}
                        <label className="block text-gray-700 font-bold mb-2" htmlFor="numeros">
                            Numbers
                        </label>
                        <input
                            className={`border ${Errors.Number.length > 0 ? 'border-red-500' : ''} rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none`}
                            id="numeros"
                            name="Number"
                            type="text"
                            placeholder="1,2,3,4,5,6 etc..."
                            onChange={Change}
                            value={Enviar.Number}
                        />
                    </div>
                    <div className="mb-1 relative">
                        {Errors.Season.map((error) => (
                            <div className=" text-red-600 flex items-center gap-1" key={error}><ImWarning className="text-red-500" />{error}</div>
                        ))}
                        <label className="block text-gray-700 font-bold mb-2" htmlFor="estaciones">
                            Seasons
                        </label>
                        <input
                            className={`border ${Errors.Season.length > 0 ? 'border-red-500' : ''} ${Errors.length === 0 ? 'border-green-500' : ''} rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none`}
                            id="estaciones"
                            name="Season"
                            type="text"
                            placeholder="Winter Summer..."
                            onChange={Change}
                            value={Enviar.Season}
                        />
                    </div>
                    <div className="flex items-center justify-center p-4">
                        <button className="bg-blue-500 w-[100px] hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit"> Send</button>
                    </div>
                </div>
            </form>
        </>
    )
}
