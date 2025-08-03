// Enums
const City = Object.freeze({
  Bangalore: 'Bangalore',
  Delhi: 'Delhi'
});

const SeatCategory = Object.freeze({
  SILVER: 'SILVER',
  GOLD: 'GOLD',
  PLATINUM: 'PLATINUM'
});

class Seat {
  constructor() {
    this.seatId = null;
    this.row = 0;
    this.seatCategory = null;
  }
}

class Screen {
  constructor() {
    this.screenId = null;
    this.seats = [];
  }
}

class Movie {
  constructor() {
    this.movieId = 0;
    this.movieName = '';
    this.movieDurationInMinutes = 0;
  }
}

class MovieController {
  constructor() {
    this.cityWiseMovies = new Map();
    this.allMovies = [];
  }

  addMovie(movie, city) {
    this.allMovies.push(movie);
    if (!this.cityWiseMovies.has(city)) {
      this.cityWiseMovies.set(city, []);
    }
    this.cityWiseMovies.get(city).push(movie);
  }

  getMovieByName(name) {
    return this.allMovies.find(m => m.movieName === name);
  }

  getMoviesByCity(city) {
    return this.cityWiseMovies.get(city) || [];
  }
}

class Show {
  constructor() {
    this.showId = 0;
    this.movie = null;
    this.screen = null;
    this.showStartTime = 0;
    this.bookedSeatsIds = [];
  }
}

class Booking {
  constructor() {
    this.show = null;
    this.bookedSeats = [];
    this.payment = null;
  }
}

class Payment {
  constructor() {
    this.paymentId = 0;
  }
}

class Theatre {
  constructor() {
    this.theatreId = 0;
    this.address = null;
    this.city = null;
    this.screens = [];
    this.shows = [];
  }
}

class TheatreController {
  constructor() {
    this.cityWiseTheatre = new Map();
    this.allTheatre = [];
  }

  addTheatre(theatre, city) {
    this.allTheatre.push(theatre);
    if (!this.cityWiseTheatre.has(city)) {
      this.cityWiseTheatre.set(city, []);
    }
    this.cityWiseTheatre.get(city).push(theatre);
  }

  getAllShow(movie, city) {
    const theatreWiseShows = new Map();
    const theatres = this.cityWiseTheatre.get(city) || [];

    for (const theatre of theatres) {
      const givenMovieShows = theatre.shows.filter(show => show.movie.movieName === movie.movieName);
      if (givenMovieShows.length > 0) {
        theatreWiseShows.set(theatre, givenMovieShows);
      }
    }

    return theatreWiseShows;
  }
}

class BookMyShow {
  constructor() {
    this.movieController = new MovieController();
    this.theatreController = new TheatreController();
  }

  main() {
    this.initialize();

    this.createBooking(City.Bangalore, 'BAAHUBALI');
    this.createBooking(City.Bangalore, 'BAAHUBALI');
  }

  createBooking(userCity, movieName) {
    const movies = this.movieController.getMoviesByCity(userCity);
    const interestedMovie = movies.find(movie => movie.movieName === movieName);

    const showsTheatreWise = this.theatreController.getAllShow(interestedMovie, userCity);
    const [firstEntry] = showsTheatreWise.entries();

    if (!firstEntry) return;

    const [_, runningShows] = firstEntry;
    const interestedShow = runningShows[0];

    const seatNumber = 30;
    const bookedSeats = interestedShow.bookedSeatsIds;

    if (!bookedSeats.includes(seatNumber)) {
      bookedSeats.push(seatNumber);

      const booking = new Booking();
      const myBookedSeats = interestedShow.screen.seats.filter(seat => seat.seatId === seatNumber);

      booking.bookedSeats = myBookedSeats;
      booking.show = interestedShow;

      console.log('BOOKING SUCCESSFUL');
    } else {
      console.log('seat already booked, try again');
    }
  }

  initialize() {
    this.createMovies();
    this.createTheatre();
  }

  createMovies() {
    const avengers = new Movie();
    avengers.movieName = 'AVENGERS';
    avengers.movieDurationInMinutes = 128;

    const baahubali = new Movie();
    baahubali.movieName = 'BAAHUBALI';
    baahubali.movieDurationInMinutes = 180;

    [City.Bangalore, City.Delhi].forEach(city => {
      this.movieController.addMovie(avengers, city);
      this.movieController.addMovie(baahubali, city);
    });
  }

  createTheatre() {
    const avengerMovie = this.movieController.getMovieByName('AVENGERS');
    const baahubaliMovie = this.movieController.getMovieByName('BAAHUBALI');

    const inoxTheatre = new Theatre();
    inoxTheatre.theatreId = 1;
    inoxTheatre.city = City.Bangalore;
    inoxTheatre.screens = this.createScreen();
    inoxTheatre.shows = [
      this.createShow(1, inoxTheatre.screens[0], avengerMovie, 8),
      this.createShow(2, inoxTheatre.screens[0], baahubaliMovie, 16)
    ];

    const pvrTheatre = new Theatre();
    pvrTheatre.theatreId = 2;
    pvrTheatre.city = City.Delhi;
    pvrTheatre.screens = this.createScreen();
    pvrTheatre.shows = [
      this.createShow(3, pvrTheatre.screens[0], avengerMovie, 13),
      this.createShow(4, pvrTheatre.screens[0], baahubaliMovie, 20)
    ];

    this.theatreController.addTheatre(inoxTheatre, City.Bangalore);
    this.theatreController.addTheatre(pvrTheatre, City.Delhi);
  }

  createScreen() {
    const screen = new Screen();
    screen.screenId = 1;
    screen.seats = this.createSeats();
    return [screen];
  }

  createShow(showId, screen, movie, time) {
    const show = new Show();
    show.showId = showId;
    show.screen = screen;
    show.movie = movie;
    show.showStartTime = time;
    return show;
  }

  createSeats() {
    const seats = [];

    for (let i = 0; i < 40; i++) {
      const seat = new Seat();
      seat.seatId = i;
      seat.seatCategory = SeatCategory.SILVER;
      seats.push(seat);
    }

    for (let i = 40; i < 70; i++) {
      const seat = new Seat();
      seat.seatId = i;
      seat.seatCategory = SeatCategory.GOLD;
      seats.push(seat);
    }

    for (let i = 70; i < 100; i++) {
      const seat = new Seat();
      seat.seatId = i;
      seat.seatCategory = SeatCategory.PLATINUM;
      seats.push(seat);
    }

    return seats;
  }
}

const app = new BookMyShow();
app.main();
