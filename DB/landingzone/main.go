package main

import (
	"log"
	"net"

	"github.com/seadsystem/Backend/DB/landingzone/constants"
	"github.com/seadsystem/Backend/DB/landingzone/database"
	"github.com/seadsystem/Backend/DB/landingzone/decoders"
	"github.com/seadsystem/Backend/DB/landingzone/handlers"
)

func main() {
	listener, err := net.Listen("tcp4", constants.HOST+":"+constants.PORT) // The plugs only support IPv4.
	if err != nil {
		log.Println("Failed to open listener on port " + constants.PORT)
		log.Panic("Error was: " + err.Error())
	}
	defer listener.Close()

	// Setup database routine
	database_channel := make(chan decoders.SeadPacket, 10) // Allows buffering up to 10 SeadPackets
	db, err := database.New()
	go db.InsertRaw(database_channel)

	log.Println("Listening for connections...")

	// Handle requests in a go routine
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println("Failed to accept request: " + err.Error())
			continue
		}
		go handlers.HandleRequest(conn, database_channel)
	}
}
