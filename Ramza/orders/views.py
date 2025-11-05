import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.db import transaction
import json
import uuid
from decimal import Decimal
from .models import Order, OrderItem
from restaurant.models import MenuItem

# Set up logging
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def create_order_and_redirect_whatsapp(request):
    """
    Create an order in the database and redirect to WhatsApp with order details
    """
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Extract order details
        customer_name = data.get('customer_name', '')
        customer_phone = data.get('customer_phone', '')
        customer_email = data.get('customer_email', '')
        delivery_method = data.get('delivery_method', 'delivery')
        delivery_address = data.get('delivery_address', '')
        cart_items = data.get('cart_items', [])
        subtotal = Decimal(str(data.get('subtotal', '0.00')))
        delivery_fee = Decimal(str(data.get('delivery_fee', '0.00')))
        total = Decimal(str(data.get('total', '0.00')))
        
        # Use database transaction to ensure data consistency
        with transaction.atomic():
            # Create the order with initial status
            order = Order(
                order_number=f'ORD-{uuid.uuid4().hex[:8].upper()}',
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email,
                order_type=delivery_method,
                delivery_address=delivery_address,
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                total=total,
                # Set initial status to indicate order was sent to WhatsApp
                status='sent_to_whatsapp',  # New status
                payment_status='pending'
            )
            order.save()
            
            # Log order creation
            logger.info(f"Order created: {order.order_number} for customer {customer_name}")
            
            # Create order items
            for item_data in cart_items:
                menu_item_id = item_data.get('id')
                quantity = item_data.get('quantity', 1)
                
                try:
                    menu_item = MenuItem.objects.get(id=menu_item_id)
                    order_item = OrderItem(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        price=menu_item.price
                    )
                    order_item.save()
                    logger.info(f"Order item created: {quantity}x {menu_item.name} for order {order.order_number}")
                except MenuItem.DoesNotExist:
                    # Skip items that don't exist
                    logger.warning(f"Menu item with ID {menu_item_id} not found, skipping")
                    continue
            
            # Format WhatsApp message
            whatsapp_message = f"New Order Request\n"
            whatsapp_message += f"Name: {customer_name}\n"
            whatsapp_message += f"Phone: {customer_phone}\n"
            whatsapp_message += f"Order ID: #{order.order_number}\n"
            whatsapp_message += f"Items:\n\n"
            
            for item_data in cart_items:
                try:
                    menu_item = MenuItem.objects.get(id=item_data.get('id'))
                    item_total = menu_item.price * item_data.get('quantity', 1)
                    whatsapp_message += f"{menu_item.name} (x{item_data.get('quantity')}) — R{item_total:.2f}\n"
                except MenuItem.DoesNotExist:
                    continue
            
            whatsapp_message += f"\nTotal: R{total:.2f}\n"
            
            if delivery_method == 'delivery' and delivery_address:
                whatsapp_message += f"Delivery Address: {delivery_address}\n"
            else:
                whatsapp_message += f"Pickup Order\n"
            
            whatsapp_message += f"Payment: Cash on Delivery\n"
            
            # Encode the message for URL
            import urllib.parse
            encoded_message = urllib.parse.quote(whatsapp_message)
            
            # WhatsApp URL
            whatsapp_url = f"https://wa.me/27816299491?text={encoded_message}"
            
            # Log successful order creation
            logger.info(f"Order {order.order_number} successfully created and committed to database")
            
            # Return success response with WhatsApp URL
            return JsonResponse({
                'success': True,
                'whatsapp_url': whatsapp_url,
                'order_id': order.order_number
            })
        
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def get_order_status(request, order_id):
    """
    Get order status and details by order ID
    """
    try:
        # Try to find order by order_number first, then by id
        try:
            order = Order.objects.get(order_number=order_id)
        except Order.DoesNotExist:
            # If not found by order_number, try to find by id
            try:
                order_id_int = int(order_id)
                order = Order.objects.get(id=order_id_int)
            except (ValueError, Order.DoesNotExist):
                logger.warning(f"Order not found: {order_id}")
                return JsonResponse({
                    'success': False,
                    'error': 'Order not found'
                }, status=404)
        
        # Log successful order retrieval
        logger.info(f"Order status retrieved: {order.order_number}")
        
        # Prepare order details
        order_items = []
        for item in order.items.all():
            order_items.append({
                'name': item.menu_item.name,
                'quantity': item.quantity,
                'price': float(item.price),
                'total': float(item.total_price)
            })
        
        order_data = {
            'id': order.id,
            'order_number': order.order_number,
            'customer_name': order.customer_name,
            'customer_phone': order.customer_phone,
            'customer_email': order.customer_email,
            'order_type': order.order_type,
            'delivery_address': order.delivery_address,
            'status': order.status,
            'status_display': order.get_status_display(),
            'payment_status': order.payment_status,
            'subtotal': float(order.subtotal),
            'delivery_fee': float(order.delivery_fee),
            'total': float(order.total),
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat(),
            'items': order_items
        }
        
        return JsonResponse({
            'success': True,
            'order': order_data
        })
        
    except Exception as e:
        logger.error(f"Error retrieving order status: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def list_orders(request):
    """
    List all orders with basic information for tracking page
    """
    try:
        # Get all orders, ordered by creation date (newest first)
        orders = Order.objects.all().order_by('-created_at')
        
        # Log successful order list retrieval
        logger.info(f"Retrieved {orders.count()} orders for tracking page")
        
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'order_number': order.order_number,
                'customer_name': order.customer_name,
                'customer_phone': order.customer_phone,  # Add customer phone
                'status': order.status,
                'status_display': order.get_status_display(),
                'total': float(order.total),
                'created_at': order.created_at.isoformat(),
                'updated_at': order.updated_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'orders': orders_data
        })
        
    except Exception as e:
        logger.error(f"Error listing orders: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def update_order_status_api(request, order_id):
    """
    Update order status via API
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Method not allowed'
        }, status=405)
    
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get('status', request.GET.get('status'))
        
        if not new_status:
            # Try to get from JSON body
            try:
                data = json.loads(request.body)
                new_status = data.get('status')
            except:
                pass
        
        if not new_status:
            return JsonResponse({
                'success': False,
                'error': 'Status is required'
            }, status=400)
        
        # Validate status
        valid_statuses = [choice[0] for choice in Order.ORDER_STATUS_CHOICES]
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'error': f'Invalid status. Valid statuses: {", ".join(valid_statuses)}'
            }, status=400)
        
        old_status = order.status
        order.status = new_status
        order.save()
        
        # If status changed, send WhatsApp notification
        if old_status != new_status:
            send_whatsapp_status_update(order, new_status)
        
        return JsonResponse({
            'success': True,
            'status': new_status,
            'message': f'Order status updated to {order.get_status_display()}'
        })
        
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Order not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def send_whatsapp_status_update(order, new_status):
    """
    Send WhatsApp message to customer when order status changes
    """
    try:
        # Map status to user-friendly message
        status_messages = {
            'sent_to_whatsapp': 'Your order has been received and sent to our admin team!',
            'confirmed': 'Your order has been confirmed and is being prepared.',
            'preparing': 'Your order is now being prepared.',
            'ready': 'Your order is ready for pickup/delivery.',
            'out_for_delivery': 'Your order is out for delivery.',
            'delivered': 'Your order has been delivered. Enjoy your meal!',
            'completed': 'Your order is complete. Thank you for choosing us!',
            'cancelled': 'Unfortunately, your order has been cancelled.'
        }
        
        # Create status update message
        message = f"Order Status Update\n"
        message += f"Order ID: #{order.order_number}\n"
        message += f"Status: {order.get_status_display()}\n"
        message += f"Update: {status_messages.get(new_status, 'Your order status has been updated.')}\n"
        message += f"Thank you for choosing Ramza's Chillas!"
        
        # Encode message for URL
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        
        # Send to customer's phone number
        whatsapp_url = f"https://wa.me/{order.customer_phone}?text={encoded_message}"
        
        # In a real implementation, we would send this via WhatsApp API
        # For now, we're just logging it
        print(f"Would send WhatsApp update to {order.customer_phone}: {message}")
        
        return True
    except Exception as e:
        print(f"Error sending WhatsApp update: {str(e)}")
        return False

# Add the CSRF exempt decorator to the update_order_status_api function
update_order_status_api = csrf_exempt(update_order_status_api)