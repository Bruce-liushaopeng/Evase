function Ping(props) {

    return (
        <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-slate-400 dark:bg-slate-200"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-slate-500 dark:bg-slate-300"></span>
        </span>
    )
}

export default Ping;