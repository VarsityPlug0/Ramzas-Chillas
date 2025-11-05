# ZAR Pricing Confirmation

This document confirms that all prices in the Ramza's Chillas application are stored and displayed in South African Rand (ZAR).

## Implementation Details

1. **Database Storage**: 
   - Prices are stored in the `MenuItem.price` field as `DecimalField` with 2 decimal places
   - The field has explicit help text: "Price in Rand (e.g., 12.99)"
   - Migration [0004_alter_menuitem_price.py](file:///c%3A/Users/money/Bevan%20The%20IT%20GUY/absa/ramzas-chillas/restaurant/migrations/0004_alter_menuitem_price.py) confirms the currency specification

2. **Frontend Display**:
   - Menu items display prices with "R" prefix: `R{{ item.price }}`
   - Cart items display prices with "R" prefix: `R${item.price}`
   - Checkout displays prices with "R" prefix: `R${(item.price * item.quantity).toFixed(2)}`

3. **Currency Symbol**:
   - The "R" symbol is the official currency symbol for South African Rand
   - All price displays use this symbol correctly

## Verification

All prices in the application are confirmed to be in South African Rand (ZAR).