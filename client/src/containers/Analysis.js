import Upload from "./Upload";

function Analysis(props) {

    return (
        <div className="flex flex-row bg-gray-200 rounded-xl shadow border p-20 align-center pl-40 min-h-screen">
            <header className="uploadInstruction">
                <p>{props.instruction}</p>
            </header>
            <div>
                <input id="default-radio-1" type="radio" value="" name="sql-radio" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                    SQL Injection
                </input>
                <input id="default-radio-1" type="radio" value="" name="forced-deadlock-radio" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                    Forced Deadlock
                </input>
                <input id="default-radio-1" type="radio" value="" name="no-encryption-radio" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                    Lack of Password Encryption
                </input>
                <input id="default-radio-1" type="radio" value="" name="password-guessing-radio" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                    Brute Force Password Attacks
                </input>
            </div>
        </div>
    );
}

export default Upload;