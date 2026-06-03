document
.getElementById("predictBtn")
.addEventListener("click", async () => {

    const data = {

        brand:
        document.getElementById("brand").value,

        os:
        document.getElementById("os").value,

        screen_size:
        Number(
            document.getElementById("screen_size").value
        ),

        weight:
        Number(
            document.getElementById("weight").value
        ),

        ram:
        Number(
            document.getElementById("ram").value
        ),

        internal_memory:
        Number(
            document.getElementById("storage").value
        ),

        battery:
        Number(
            document.getElementById("battery").value
        ),

        days_used:
        Number(
            document.getElementById("days_used").value
        ),

        rear_camera_mp:
        Number(
            document.getElementById("rear_camera").value
        ),

        front_camera_mp:
        Number(
            document.getElementById("front_camera").value
        ),

        release_year:
        Number(
            document.getElementById("release_year").value
        ),

        normalized_new_price:
        Number(
            document.getElementById("new_price").value
        ),

        fourg:
        Number(
            document.getElementById("fourg").value
        ),

        fiveg:
        Number(
            document.getElementById("fiveg").value
        )
    };

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body:
                JSON.stringify(data)
            }
        );

        const result =
        await response.json();

        document
        .getElementById("resaleValue")
        .innerHTML =
        "₹ " +
        result.resale_value;

        document
        .getElementById("recycleValue")
        .innerHTML =
        "₹ " +
        result.recycling_value;

        document
        .getElementById("recommendation")
        .innerHTML =
        result.recommendation;

        document
        .getElementById("gold")
        .innerHTML =
        "Gold : " +
        result.gold +
        " g";

        document
        .getElementById("silver")
        .innerHTML =
        "Silver : " +
        result.silver +
        " g";

        document
        .getElementById("copper")
        .innerHTML =
        "Copper : " +
        result.copper +
        " g";

        document
        .getElementById("lithium")
        .innerHTML =
        "Lithium : " +
        result.lithium +
        " g";

    }

    catch(error){

        console.error(error);

        alert(
            "Backend connection failed."
        );
    }

});