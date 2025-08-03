from enum import Enum

class City(Enum):
    Bangalore = 'Bangalore'
    Delhi = 'Delhi'

class SeatCategory(Enum):
    SILVER = 'SILVER'
    GOLD = 'GOLD'
    PLATINUM = 'PLATINUM'

class Seat:
    seatId = None
    row = 0
    seatCategory = None

    def getSeatId(self):
        return self.seatId
    
    def setSeatId(self, seatId):
        self.seatId = seatId

    def getRow(self):
        return self.row

    def setRow(self, row):
        self.row = row
    
    def getSeatCategory(self):
        return self.seatCategory

    def setSeatCategory(self, seatCategory):
        self.seatCategory = seatCategory

class Screen:
    screenId = None
    seats = []

    def getScreenId(self):
        return self.screenId
    
    def setScreenId(self, screenId):
        self.screenId = screenId

    def getSeats(self):
        return self.seats
    
    def setSeats(self, seats):
        self.seats = seats

class Movie:
    movieId = 0
    movieName = ''
    movieDurationInMinutes = 0
    # other details like genre, language, etc.

    def getMovieId(self):
        return self.movieId
    
    def setMovieId(self, movieId):
        self.movieId = movieId
    
    def getMovieName(self):
        return self.movieName
    
    def setMovieName(self, movieName):
        self.movieName = movieName

    def getMovieDuration(self):
        return self.movieDurationInMinutes
    
    def setMovieDuration(self, movieDuration):
        self.movieDurationInMinutes = movieDuration

from collections import defaultdict
class MovieController:
    cityWiseMovies = None
    allMovies = None

    def __init__(self):
        self.cityWiseMovies = defaultdict(list)
        self.allMovies = []

    # add movie to a particular city, make use of cityWiseMovies map
    def addMovie(self, movie, city):
        self.allMovies.append(movie)

        movies = self.cityWiseMovies[city]
        movies.append(movie)
        self.cityWiseMovies[city] = movies

    def getMovieByName(self, movieName):
        for movie in self.allMovies:
            if movie.getMovieName() == movieName:
                return movie
        
        return None
    
    def getMoviesByCity(self, city):
        return self.cityWiseMovies[city]
    
    # REMOVE movie from a particular city, make use of cityVsMovies map

    # UPDATE movie of a particular city, make use of cityVsMovies map

    # CRUD operation based on Movie ID, make use of allMovies list

class Show:
    showId = 0
    movie = None
    screen = None
    showStartTime = 0
    bookedSeatsIds = []

    def getShowId(self):
        return self.showId
    
    def setShowId(self, showId):
        self.showId = showId

    def getMovie(self):
        return self.movie
    
    def setMovie(self, movie):
        self.movie = movie

    def getScreen(self):
        return self.screen
    
    def setScreen(self, screen):
        self.screen = screen

    def getShowStartTime(self):
        return self.showStartTime
    
    def setShowStartTime(self, showStartTime):
        self.showStartTime = showStartTime

    def getBookedSeatIds(self):
        return self.bookedSeatsIds
    
    def setBoookedSeatIds(self, bookedSeatsId):
        self.bookedSeatsIds = bookedSeatsId

class Booking:
    show = None
    bookedSeats = []
    payment = None

    def getShow(self):
        return self.show
    
    def setShow(self, show):
        self.show = show

    def getBookedSeats(self):
        return self.bookedSeats
    
    def setBookedSeats(self, bookedSeats):
        self.bookedSeats = bookedSeats

    def getPayment(self):
        return self.payment
    
    def setPayment(self, payment):
        self.payment = payment

class Payment:

    paymentId = 0
    # other payment details

class Theatre:
    theatreId = 0
    address = None
    city = None
    screen = None
    shows = None

    def getTheatreId(self):
        return self.theatreId
    
    def setTheatreId(self, theatreId):
        self.theatreId = theatreId

    def getAddress(self):
        return self.address

    def setAddress(self, address):
        self.address = address

    def getCity(self):
        return self.city
    
    def setCity(self, city):
        self.city = city

    def getScreen(self):
        return self.screen
    
    def setScreen(self, screen):
        self.screen = screen

    def getShows(self):
        return self.shows
    
    def setShows(self, shows):
        self.shows = shows

class TheatreController:
    cityWiseTheatre = None
    allTheatre = None

    def __init__(self):
        self.cityWiseTheatre = defaultdict(list)
        self.allTheatre = []

    def addTheatre(self, theatre, city):
        self.allTheatre.append(theatre)

        theatres = self.cityWiseTheatre[city]
        theatres.append(theatre)
        self.cityWiseTheatre[city] = theatres
    
    def getAllShow(self, movie, city):
        # get all the theatres of this city

        theatreWiseShows = defaultdict(list)
        theatres = self.cityWiseTheatre[city]

        # filter the threatres which run this movie
        for theatre in theatres:
            givenMovieShows = []
            shows = theatre.getShows()

            for show in shows:
                if show.movie.getMovieId() == movie.getMovieId():
                    givenMovieShows.append(show)
            
            if len(givenMovieShows) > 0:
                theatreWiseShows[theatre] = givenMovieShows
        
        return theatreWiseShows
    
class BookMyShow:
    movieController = None
    theatreController = None

    def __init__(self):
        self.movieController = MovieController()
        self.theatreController = TheatreController()

    def main(self):
        bookMyShow = BookMyShow()
        bookMyShow.initialize()

        # user1
        bookMyShow.createBooking(City.Bangalore, 'BAAHUBALI')

        # user2
        bookMyShow.createBooking(City.Bangalore, 'BAAHUBALI')

    def createBooking(self, userCity, movieName):
        # 1. search movie by my location
        movies = self.movieController.getMoviesByCity(userCity)

        # 2. select the movie which you want to see. I want to see Baahubali
        interestedMovie = None
        for movie in movies:
            if movie.getMovieName() == movieName:
                interestedMovie = movie
        
        # 3. get al show of this movie in bangalore location
        showsTheatreWise = self.theatreController.getAllShow(interestedMovie, userCity)

        # 4. select the particular show user is interested in
        entry = next(iter(showsTheatreWise.items()), None)
        _, running_shows = entry
        interestedShow = running_shows[0]

        # 5. select the seat
        seatNumber = 30
        bookedSeats = interestedShow.getBookedSeatIds()

        if seatNumber not in bookedSeats:
            bookedSeats.append(seatNumber)

            # start payment
            booking = Booking()
            myBookedSeats = []
            for screenSeat in interestedShow.getScreen().getSeats():
                if screenSeat.getSeatId() == seatNumber:
                    myBookedSeats.append(screenSeat)
            
            booking.setBookedSeats(myBookedSeats)
            booking.setShow(interestedShow)

        else:
            print('seat already booked, try again')
            return
    
        print('BOOKING SUCCESSFUL')
    
    def initialize(self):
        # create movies
        self.createMovies()

        # create theatre with screens, seats and shows
        self.createTheatre()

    # creating theatre 2
    def createTheatre(self):
        avengerMovie = self.movieController.getMovieByName('AVENGERS')
        baahubaliMovie = self.movieController.getMovieByName('BAAHUBALI')

        inoxTheatre = Theatre()
        inoxTheatre.setTheatreId(1)
        inoxTheatre.setScreen(self.createScreen())
        inoxTheatre.setCity(City.Bangalore)
        inoxShows = []
        inoxMorningShow = self.createShows(1, inoxTheatre.getScreen()[0], avengerMovie, 8)
        inoxEveningShow = self.createShows(2, inoxTheatre.getScreen()[0], baahubaliMovie, 16)
        inoxShows.append(inoxMorningShow)
        inoxShows.append(inoxEveningShow)
        inoxTheatre.setShows(inoxShows)

        pvrTheatre = Theatre()
        pvrTheatre.setTheatreId(2)
        pvrTheatre.setScreen(self.createScreen())
        pvrTheatre.setCity(City.Delhi)
        pvrShows = []
        pvrMorningShow = self.createShows(3, pvrTheatre.getScreen()[0], avengerMovie, 13)
        pvrEveningShow = self.createShows(4, pvrTheatre.getScreen()[0], baahubaliMovie, 20)
        pvrShows.append(pvrMorningShow)
        pvrShows.append(pvrEveningShow)
        pvrTheatre.setShows(pvrShows)

        self.theatreController.addTheatre(inoxTheatre, City.Bangalore)
        self.theatreController.addTheatre(pvrTheatre, City.Delhi)

    def createScreen(self):
        screens = []
        screen1 = Screen()
        screen1.setScreenId(1)
        screen1.setSeats(self.createSeats())
        screens.append(screen1)

        return screens

    def createShows(self, showId, screen, movie, showStartTime):
        show = Show()
        show.setShowId(showId)
        show.setScreen(screen)
        show.setMovie(movie)
        show.setShowStartTime(showStartTime)    # 24 hrs time ex: 14 means 2pm
        return show
    
    # creating 100 seats
    def createSeats(self):
        # creating 100 seats for testing purpose
        seats = []

        # 1 to 40: SILVER
        for i in range(40):
            seat = Seat()
            seat.setSeatId(i)
            seat.setSeatCategory(SeatCategory.SILVER)
            seats.append(seat)

        # 41 to 70: GOLD
        for i in range(40, 70):
            seat = Seat()
            seat.setSeatId(i)
            seat.setSeatCategory(SeatCategory.GOLD)
            seats.append(seat)

        # 70 to 100: GOLD
        for i in range(70, 100):
            seat = Seat()
            seat.setSeatId(i)
            seat.setSeatCategory(SeatCategory.PLATINUM)
            seats.append(seat)

        return seats
    
    def createMovies(self):
        # create movie 1
        avengers = Movie()
        avengers.setMovieName('AVENGERS')
        avengers.setMovieDuration(128)

        # create movie 2
        baahubali = Movie()
        baahubali.setMovieName('BAAHUBALI')
        baahubali.setMovieDuration(180)

        # add movies against the cities
        self.movieController.addMovie(avengers, City.Bangalore)
        self.movieController.addMovie(avengers, City.Delhi)
        self.movieController.addMovie(baahubali, City.Bangalore)
        self.movieController.addMovie(baahubali, City.Delhi)

if __name__ == '__main__':
    bookMyShow = BookMyShow()
    bookMyShow.main()