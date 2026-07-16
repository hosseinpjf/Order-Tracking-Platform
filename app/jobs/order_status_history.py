from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone, timedelta
import logging
from app.models.order_status_history import OrderStatusHistory, StatusChangedBy
from app.models.order import Order, OrderStatus, OrderType


logger = logging.getLogger(__name__)

def auto_update_order_status(db: Session):
    try:
        now = datetime.now(timezone.utc)
        print(now)
        updated = False

        db_orders = (db
            .query(Order)
            .options(joinedload(Order.status_history))
            .filter(Order.status == OrderStatus.preparing)
            .with_for_update(skip_locked=True)
            .all()
        )
        due_orders = []

        for order in db_orders:
            order_status_history = next(
                (item for item in order.status_history if item.status == OrderStatus.preparing and item.end_at is None),
                None
            )

            if order_status_history is None:
                logger.error(f"Data inconsistency: order {order.id} has no open preparing history")
                continue

            start_at = order_status_history.start_at
            if start_at.tzinfo is None:
                start_at = start_at.replace(tzinfo=timezone.utc)

            if start_at + timedelta(minutes=order.total_prepare_time) < now:
                due_orders.append((order, order_status_history))

        for order, order_status_history in due_orders:
            updated = True

            new_status = OrderStatus.delivering if order.order_type == OrderType.delivery else OrderStatus.completed
            order.status = new_status

            # Old status update
            if order_status_history.start_at.tzinfo is None:
                order_status_history.start_at = order_status_history.start_at.replace(tzinfo=timezone.utc)

            order_status_history.end_at = now
            order_status_history.duration_seconds = int((now - order_status_history.start_at).total_seconds())
            order_status_history.changed_by = StatusChangedBy.system

            # Creating a new status
            new_order_status_history = OrderStatusHistory(
                order_id = order.id,
                status = new_status,
            )

            if new_status == OrderStatus.completed:
                new_order_status_history.changed_by = StatusChangedBy.system
                new_order_status_history.duration_seconds = 0
                new_order_status_history.end_at = now

            db.add(new_order_status_history)

        if updated:
            db.commit()
    except Exception:
        db.rollback()
        raise