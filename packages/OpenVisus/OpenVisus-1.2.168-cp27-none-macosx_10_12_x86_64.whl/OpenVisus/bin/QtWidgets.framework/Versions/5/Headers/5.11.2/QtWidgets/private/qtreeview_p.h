/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtWidgets module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

#ifndef QTREEVIEW_P_H
#define QTREEVIEW_P_H

//
//  W A R N I N G
//  -------------
//
// This file is not part of the Qt API.  It exists purely as an
// implementation detail.  This header file may change from version to
// version without notice, or even be removed.
//
// We mean it.
//

#include <QtWidgets/private/qtwidgetsglobal_p.h>
#include "private/qabstractitemview_p.h"
#include <QtCore/qvariantanimation.h>
#include <QtCore/qabstractitemmodel.h>
#include <QtCore/qvector.h>

QT_REQUIRE_CONFIG(treeview);

QT_BEGIN_NAMESPACE

struct QTreeViewItem
{
    QTreeViewItem() : parentItem(-1), expanded(false), spanning(false), hasChildren(false),
                      hasMoreSiblings(false), total(0), level(0), height(0) {}
    QModelIndex index; // we remove items whenever the indexes are invalidated
    int parentItem; // parent item index in viewItems
    uint expanded : 1;
    uint spanning : 1;
    uint hasChildren : 1; // if the item has visible children (even if collapsed)
    uint hasMoreSiblings : 1;
    uint total : 28; // total number of children visible
    uint level : 16; // indentation
    int height : 16; // row height
};

Q_DECLARE_TYPEINFO(QTreeViewItem, Q_MOVABLE_TYPE);

class Q_WIDGETS_EXPORT QTreeViewPrivate : public QAbstractItemViewPrivate
{
    Q_DECLARE_PUBLIC(QTreeView)
public:

    QTreeViewPrivate()
        : QAbstractItemViewPrivate(),
          header(0), indent(20), lastViewedItem(0), defaultItemHeight(-1),
          uniformRowHeights(false), rootDecoration(true),
          itemsExpandable(true), sortingEnabled(false),
          expandsOnDoubleClick(true),
          allColumnsShowFocus(false), customIndent(false), current(0), spanning(false),
          animationsEnabled(false), columnResizeTimerID(0),
          autoExpandDelay(-1), hoverBranch(-1), geometryRecursionBlock(false), hasRemovedItems(false),
          treePosition(0) {}

    ~QTreeViewPrivate() {}
    void initialize();
    int logicalIndexForTree() const;
    inline bool isTreePosition(int logicalIndex) const
    {
        return logicalIndex == logicalIndexForTree();
    }

    QItemViewPaintPairs draggablePaintPairs(const QModelIndexList &indexes, QRect *r) const override;
    void adjustViewOptionsForIndex(QStyleOptionViewItem *option, const QModelIndex &current) const override;

#ifndef QT_NO_ANIMATION
    struct AnimatedOperation : public QVariantAnimation
    {
        int item;
        QPixmap before;
        QPixmap after;
        QWidget *viewport;
        AnimatedOperation() : item(0) { setEasingCurve(QEasingCurve::InOutQuad); }
        int top() const { return startValue().toInt(); }
        QRect rect() const { QRect rect = viewport->rect(); rect.moveTop(top()); return rect; }
        void updateCurrentValue(const QVariant &) override { viewport->update(rect()); }
        void updateState(State state, State) override { if (state == Stopped) before = after = QPixmap(); }
    } animatedOperation;
    void prepareAnimatedOperation(int item, QVariantAnimation::Direction d);
    void beginAnimatedOperation();
    void drawAnimatedOperation(QPainter *painter) const;
    QPixmap renderTreeToPixmapForAnimation(const QRect &rect) const;
    void _q_endAnimatedOperation();
#endif //QT_NO_ANIMATION

    void expand(int item, bool emitSignal);
    void collapse(int item, bool emitSignal);

    void _q_columnsAboutToBeRemoved(const QModelIndex &, int, int) override;
    void _q_columnsRemoved(const QModelIndex &, int, int) override;
    void _q_modelAboutToBeReset();
    void _q_sortIndicatorChanged(int column, Qt::SortOrder order);
    void _q_modelDestroyed() override;

    void layout(int item, bool recusiveExpanding = false, bool afterIsUninitialized = false);

    int pageUp(int item) const;
    int pageDown(int item) const;

    int itemHeight(int item) const;
    int indentationForItem(int item) const;
    int coordinateForItem(int item) const;
    int itemAtCoordinate(int coordinate) const;

    int viewIndex(const QModelIndex &index) const;
    QModelIndex modelIndex(int i, int column = 0) const;

    void insertViewItems(int pos, int count, const QTreeViewItem &viewItem);
    void removeViewItems(int pos, int count);
#if 0
    bool checkViewItems() const;
#endif

    int firstVisibleItem(int *offset = 0) const;
    int lastVisibleItem(int firstVisual = -1, int offset = -1) const;
    int columnAt(int x) const;
    bool hasVisibleChildren( const QModelIndex& parent) const;

    bool expandOrCollapseItemAtPos(const QPoint &pos);

    void updateScrollBars();

    int itemDecorationAt(const QPoint &pos) const;
    QRect itemDecorationRect(const QModelIndex &index) const;


    QVector<QPair<int, int> > columnRanges(const QModelIndex &topIndex, const QModelIndex &bottomIndex) const;
    void select(const QModelIndex &start, const QModelIndex &stop, QItemSelectionModel::SelectionFlags command);

    QPair<int,int> startAndEndColumns(const QRect &rect) const;

    void updateChildCount(const int parentItem, const int delta);

    void paintAlternatingRowColors(QPainter *painter, QStyleOptionViewItem *option, int y, int bottom) const;

    // logicalIndices: vector of currently visibly logical indices
    // itemPositions: vector of view item positions (beginning/middle/end/onlyone)
    void calcLogicalIndices(QVector<int> *logicalIndices, QVector<QStyleOptionViewItem::ViewItemPosition> *itemPositions, int left, int right) const;
    int widthHintForIndex(const QModelIndex &index, int hint, const QStyleOptionViewItem &option, int i) const;
    QHeaderView *header;
    int indent;

    mutable QVector<QTreeViewItem> viewItems;
    mutable int lastViewedItem;
    int defaultItemHeight; // this is just a number; contentsHeight() / numItems
    bool uniformRowHeights; // used when all rows have the same height
    bool rootDecoration;
    bool itemsExpandable;
    bool sortingEnabled;
    bool expandsOnDoubleClick;
    bool allColumnsShowFocus;
    bool customIndent;

    // used for drawing
    mutable QPair<int,int> leftAndRight;
    mutable int current;
    mutable bool spanning;

    // used when expanding and collapsing items
    QSet<QPersistentModelIndex> expandedIndexes;
    bool animationsEnabled;

    inline bool storeExpanded(const QPersistentModelIndex &idx) {
        if (expandedIndexes.contains(idx))
            return false;
        expandedIndexes.insert(idx);
        return true;
    }

    inline bool isIndexExpanded(const QModelIndex &idx) const {
        //We first check if the idx is a QPersistentModelIndex, because creating QPersistentModelIndex is slow
        return !(idx.flags() & Qt::ItemNeverHasChildren) && isPersistent(idx) && expandedIndexes.contains(idx);
    }

    // used when hiding and showing items
    QSet<QPersistentModelIndex> hiddenIndexes;

    inline bool isRowHidden(const QModelIndex &idx) const {
        if (hiddenIndexes.isEmpty())
            return false;
        //We first check if the idx is a QPersistentModelIndex, because creating QPersistentModelIndex is slow
        return isPersistent(idx) && hiddenIndexes.contains(idx);
    }

    inline bool isItemHiddenOrDisabled(int i) const {
        if (i < 0 || i >= viewItems.count())
            return false;
        const QModelIndex index = viewItems.at(i).index;
        return isRowHidden(index) || !isIndexEnabled(index);
    }

    inline int above(int item) const
        { int i = item; while (isItemHiddenOrDisabled(--item)){} return item < 0 ? i : item; }
    inline int below(int item) const
        { int i = item; while (isItemHiddenOrDisabled(++item)){} return item >= viewItems.count() ? i : item; }
    inline void invalidateHeightCache(int item) const
        { viewItems[item].height = 0; }

    inline int accessibleTable2Index(const QModelIndex &index) const {
        return (viewIndex(index) + (header ? 1 : 0)) * model->columnCount()+index.column();
    }

    int accessibleTree2Index(const QModelIndex &index) const;

    void updateIndentationFromStyle();

    // used for spanning rows
    QVector<QPersistentModelIndex> spanningIndexes;

    // used for updating resized columns
    int columnResizeTimerID;
    QList<int> columnsToUpdate;

    // used for the automatic opening of nodes during DND
    int autoExpandDelay;
    QBasicTimer openTimer;

    // used for drawing hilighted expand/collapse indicators
    mutable int hoverBranch;

    // used for blocking recursion when calling setViewportMargins from updateGeometries
    bool geometryRecursionBlock;

    // If we should clean the set
    bool hasRemovedItems;

    // tree position
    int treePosition;
};

QT_END_NAMESPACE

#endif // QTREEVIEW_P_H
