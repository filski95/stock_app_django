Stock checking app.

Lets user search any stock available on yahoo, see the current details, add to the watchlist to monitor changes.

It provides a detail view to each of the stocks from user's watchlists with more detailed info/graphs. 

Additional stock info can be easily done through yfinance library in stocks_app->views->prepare_detailed_stock_info.

--------

App has a small name suggestions system, which helps user provide correct ticker/stock abbreviation into the app.

If a certain user added a stock, say "MANU", to the watchlist, it is saved to the db and subsequently added to the trie.-> admin_utils

If next user types in MANU1 by mistake, or MAN1 etc. they will be provided with a name sugestion.

For the system to work it is necessary to use "Load Stock Suggestion" button on the page -> admin only. This is because the Trie is being created upon running a function and is not stored in db directly (data read off db each call.)